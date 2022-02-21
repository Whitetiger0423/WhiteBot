[invite]: https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot%20applications.commands
[discord-server]: https://discord.gg/aebSVBgzuG
[discord-shield]: https://img.shields.io/discord/795837553684774933?color=7289DA&label=Official%20Discord%20Server&logo=discord&logoColor=7289DA&style=flat-square&link=https://discord.gg/aebSVBgzuG
[servercount-shield]: https://koreanbots.dev/api/widget/bots/servers/782777035898617886.svg?icon=true&scale=1&style=flat
[stars-shield]: https://img.shields.io/github/stars/dev-White-team/WhiteBot?style=flat-square&logo=github
[issues]: https://github.com/dev-White-team/WhiteBot/issues
[pulls]: https://github.com/dev-white-team/WhiteBot/pulls
[contributing]: https://github.com/dev-White-team/WhiteBot/blob/main/CONTRIBUTING.md

# WhiteBot

![servercount][servercount-shield]
![Official Discord][discord-shield]
![GitHub Repo stars][stars-shield]

슬래시로 작동하는 유틸리티 만능 봇!\
번역, 검색, 날씨와 암호화 기능까지 - [여러 유용한 기능들을 채팅하면서 바로 써보세요][invite]!

## 특징

- 디스코드의 Slash Command 기능 사용으로, `/`만 누르면 모든 명령어가 한번에 나옵니다.
- 번역, 암호화, 날씨 등 실제 채팅할때 유용한 기능들을 담았습니다.
- 가위바위보 등 혼자서 할 수 있는 놀이부터, 2인전이 가능한 틱택토까지!

## 라이선스

WhiteBot의 모든 코드는 GPL v3에 따라 보호됩니다.

## 시작하기

`/help` 명령어의 사용으로 기본 명령어의 확인이 가능합니다.

### 유틸리티 명령어

| 명령어        | 설명 |
| ------------ | --- |
| `/help`      | 봇의 도움말을 표시합니다. |
| `/search`    | 검색어를 검색합니다. 구글, 네이버, 다음, 지식백과, 위키백과, 나무위키의 검색 결과가 표시됩니다. |
| `/send`      | 항목을 임베드 형식으로 전송합니다. 줄바꿈은 적용되지 않습니다. |
| `/code`      | 수신문을 암호화합니다. base16, base32, base64, base85, 아스키 코드로의 변환이 가능합니다. |
| `/decode`    | 암호문을 해독합니다. base16, base32, base64, base85, 아스키 코드로부터의 변환이 가능합니다. |
| `/weather`   | 지역의 현재 날씨, 풍향 등을 조회합니다. |
| `/translate` | 수신문을 번역합니다. 한영, 영한, 한일, 일한, 한중, 중한 번역이 지원됩니다. |
| `/vote`      | 투표를 시작합니다. |
| `/end_vote`  | 투표를 종료합니다. |

### 관리 명령어

| 명령어     | 설명 |
| --------- | --- |
| `/bot`    | 봇의 정보를 전송합니다. 봇의 버전, 업타임 등이 같이 표시됩니다. |
| `/ping`   | 봇의 핑을 전송합니다. |
| `/delete` | 메시지를 청소합니다. 메시지 관리 권한이 필요합니다. |

### 놀이 명령어

| 명령어        | 설명 |
| ------------ | --- |
| `/rsp`       | 봇과 가위바위보를 합니다. |
| `/dice`      | 주사위를 굴립니다. 처음 변수만 사용하였을때는 1부터 N까지, 두번째 변수까지 사용하였을때는 N부터 n까지 굴립니다. |
| `/holjjac`   | 홀짝 게임을 시작합니다. |
| `/tictactoe` | 틱택토(삼목) 게임을 시작합니다. 2인전으로 진행됩니다. |
| `/youtube`   | 음성 채널에 유튜브 투게더를 활성화시키는 링크를 보냅니다. 음성 채널에 연결되어 있어야 작동하며, 대부분의 서버에서 정상적으로 작동하지 않습니다. |

## 기여하기

WhiteBot에 기여하는 방법에는 여러 가지가 있습니다.

- 버그를 발견하신 경우 [이슈][issues]를 열어주세요.
- 봇에 추가되기를 원하시는 기능도 언제든지 [이슈][issues]로 열어주세요.
- 위 내용들은 [공식 디스코드 서버][discord-server]에서 알려주셔도 무방합니다.

코드에 직접 기여하기를 원하신다면, 먼저 [CONTRIBUTING.md][contributing]를 자세히 읽어주세요.  
코드가 아무리 좋더라도, 가이드라인을 지키지 않으셨다면 PR이 거부될 수 있습니다 :(
