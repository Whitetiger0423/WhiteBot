# 코드 관련
버그는 [공식 디스코드 서버](https://github.com/dev-White-team/WhiteBot#%EA%B3%B5%EC%8B%9D-%EB%94%94%EC%8A%A4%EC%BD%94%EB%93%9C-%EC%84%9C%EB%B2%84) 또는 [이슈](https://github.com/dev-White-team/WhiteBot/issues)에서 제보하실 수 있으며, 새로운 기능을 코딩하신 뒤 적용하길 바라신다면 [PR](https://github.com/dev-White-team/WhiteBot/pulls)을 하실 수 있습니다.

코드의 무단 이용은 금지되며, 사용시에는 반드시 GPL v3.0 라이선스에 맞추어 사용하여야 합니다. 본 코드의 공개는 교육적인 목적을 위해서입니다. 무단 이용시 법적인 제재를 받을 수 있습니다.

# [WhiteBot](https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot%20applications.commands)
![servercount](https://koreanbots.dev/api/widget/bots/servers/782777035898617886.svg?icon=true&scale=1&style=classic) ![Official Discord](https://img.shields.io/discord/795837553684774933?color=7289DA&label=Official%20Discord%20Server&logo=discord&logoColor=7289DA&link=https://discord.gg/aebSVBgzuG) ![GitHub Repo stars](https://img.shields.io/github/stars/dev-White-team/WhiteBot?style=social)

슬래시로 작동하는 유틸리티 만능 봇!\
번역, 검색, 날씨와 암호화 기능까지 - [여러 유용한 기능들을 채팅하면서 바로 써보세요](https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot%20applications.commands)!

## 특징
- 디스코드의 Slash Command 기능 사용으로, `/`만 누르면 모든 명령어가 한번에 나옵니다.
- 번역, 암호화, 날씨 등 실제 채팅할때 유용한 기능들을 담았습니다.
- 가위바위보 등 혼자서 할 수 있는 놀이부터, 2인전이 가능한 틱택토까지!

## 시작하기
`/help` 명령어의 사용으로 기본 명령어의 확인이 가능합니다.

### 유틸리티 명령어

|명령어|설명|
|---|---|
|`/help`|봇의 도움말을 표시합니다.|
|`/search`|검색어를 검색합니다. 구글, 네이버, 다음, 지식백과, 위키백과, 나무위키의 검색 결과가 표시됩니다.|
|`/send`|항목을 임베드 형식으로 전송합니다. 줄바꿈은 적용되지 않습니다.|
|`/code`|수신문을 암호화합니다. base16, base32, base64, base85, 아스키 코드로의 변환이 가능합니다.|
|`/decode`|암호문을 해독합니다. base16, base32, base64, base85, 아스키 코드로부터의 변환이 가능합니다.|
|`/weather`|지역의 현재 날씨, 풍향 등을 조회합니다.|
|`/translate`|수신문을 번역합니다. 한영, 영한, 한일, 일한, 한중, 중한 번역이 지원됩니다.|
|`/vote`|투표를 시작합니다.|
|`/end_vote`|투표를 종료합니다.|

### 관리 명령어

|명령어|설명|
|---|---|
|`/bot`|봇의 정보를 전송합니다. 봇의 버전, 업타임 등이 같이 표시됩니다.|
|`/ping`|봇의 핑을 전송합니다.|
|`/delete`|메시지를 청소합니다. 메시지 관리 권한이 필요합니다.|

### 놀이 명령어

|명령어|설명|
|---|---|
|`/rsp`|봇과 가위바위보를 합니다.|
|`/dice`|주사위를 굴립니다. 처음 변수만 사용하였을때는 1부터 N까지, 두번째 변수까지 사용하였을때는 N부터 n까지 굴립니다.|
|`/holjjac`|홀짝 게임을 시작합니다.|
|`/tictactoe`|틱택토(삼목) 게임을 시작합니다. 2인전으로 진행됩니다.|
|`/youtube`|음성 채널에 유튜브 투게더를 활성화시키는 링크를 보냅니다. 음성 채널에 연결되어 있어야 작동하며, 대부분의 서버에서 정상적으로 작동하지 않습니다.|