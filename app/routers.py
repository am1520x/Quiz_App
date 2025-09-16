from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import json
from .state import get_or_create, RuntimeSession, Team

router = APIRouter()


async def broadcast(sess: RuntimeSession):
    payload = json.dumps({"type": "session_state", "data": sess.state.model_dump()})
    dead = []
    for ws in list(sess.host_conns | sess.player_conns):
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        sess.host_conns.discard(ws)
        sess.player_conns.discard(ws)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})


@router.get("/host/{session_id}", response_class=HTMLResponse)
async def host_page(request: Request, session_id: str):
    await get_or_create(session_id)
    return request.app.state.templates.TemplateResponse("host.html", {"request": request, "session_id": session_id})


@router.get("/player/{session_id}", response_class=HTMLResponse)
async def player_page(request: Request, session_id: str):
    await get_or_create(session_id)
    return request.app.state.templates.TemplateResponse("player.html", {"request": request, "session_id": session_id})


@router.websocket("/ws/{session_id}/host")
async def ws_host(ws: WebSocket, session_id: str):
    sess = await get_or_create(session_id)
    await ws.accept()
    sess.host_conns.add(ws)
    await broadcast(sess)
    try:
        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)
            async with sess.lock:
                await handle_host_action(sess, msg)
            await broadcast(sess)
    except WebSocketDisconnect:
        sess.host_conns.discard(ws)


@router.websocket("/ws/{session_id}/player")
async def ws_player(ws: WebSocket, session_id: str):
    sess = await get_or_create(session_id)
    qp = ws.scope.get("query_string", b"").decode()
    name = None
    if qp.startswith("name="):
        name = qp[5:].strip()[:32]
    await ws.accept()

    async with sess.lock:
        if not name:
            await ws.send_text(json.dumps({"type": "error", "message": "Missing team name"}))
            await ws.close()
            return
        if name in sess.state.teams:
            # Check if this name already has an active connection
            active_names = {t for conn in sess.player_conns for t in sess.state.teams if t == name}
            if active_names:
                # Another client already using this team name → reject
                await ws.send_text(json.dumps({"type": "error", "message": "Team name already taken"}))
                await ws.close()
                return
            else:
                # Same name exists in teams, but no active connection → allow reconnection
                sess.player_conns.add(ws)
        else:
            # Brand new team
            sess.state.teams[name] = Team(name=name)
            sess.player_conns.add(ws)


    await broadcast(sess)

    try:
        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)
            if msg.get("type") == "buzz":
                async with sess.lock:
                    st = sess.state
                    if st.open_for_buzz and name not in st.buzz_order and st.answered_correctly is None:
                        st.buzz_order.append(name)
                await broadcast(sess)
    except WebSocketDisconnect:
        sess.player_conns.discard(ws)
        await broadcast(sess)


async def handle_host_action(sess: RuntimeSession, msg: dict):
    st = sess.state
    t = msg.get("type")
    if t == "open_buzz":
        st.open_for_buzz = True
        st.buzz_order = []
        st.turn_index = 0
        st.answered_correctly = None
    elif t == "close_buzz":
        st.open_for_buzz = False
    elif t == "mark_correct":
        if st.buzz_order and st.turn_index < len(st.buzz_order):
            winner = st.buzz_order[st.turn_index]
            st.answered_correctly = winner
            # award 1 point to the winner
            st.teams[winner].score += 1
        st.open_for_buzz = False
    elif t == "mark_wrong":
        if st.turn_index + 1 < len(st.buzz_order):
            st.turn_index += 1
    elif t == "next_question":
        if st.question_idx + 1 < st.total_questions:
            st.question_idx += 1
            st.open_for_buzz = False
            st.buzz_order = []
            st.turn_index = 0
            st.answered_correctly = None
        else:
            st.open_for_buzz = False
    elif t == "reset_round":
        st.question_idx = 0
        st.open_for_buzz = False
        st.buzz_order = []
        st.turn_index = 0
        st.answered_correctly = None

    elif t == "reset_scores":
        for team in st.teams.values():
            team.score = 0
