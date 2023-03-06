[invite]: https://discord.com/oauth2/authorize?client_id=782777035898617886&permissions=8&scope=bot%20applications.commands
[invite-shield]: https://img.shields.io/badge/초대-하기-blue?style=flat-square
[discord-server]: https://discord.gg/EEbNMAd9vv
[discord-shield]: https://img.shields.io/discord/795837553684774933?style=flat-square&label=디스코드&logo=discord&logoColor=white
[koreanbots]: https://koreanbots.dev/bots/782777035898617886
[koreanbots-shield]: https://koreanbots.dev/api/widget/bots/servers/782777035898617886.svg
[license]: https://github.com/Whitetiger0423/WhiteBot/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/Whitetiger0423/WhiteBot?style=flat-square&label=라이선스
[stars-shield]: https://img.shields.io/github/stars/Whitetiger0423/WhiteBot?style=flat-square&label=스타&color=yellow
[python-shield]: https://img.shields.io/badge/파이썬-3.8_|_3.9_|_3.10-blue?style=flat-square&logo=python&logoColor=white
[issues]: https://github.com/Whitetiger0423/WhiteBot/issues
[pulls]: https://github.com/Whitetiger0423/WhiteBot/pulls
[contributing]: https://github.com/Whitetiger0423/WhiteBot/blob/main/CONTRIBUTING.md

# WhiteBot

[![Server Count][koreanbots-shield]][koreanbots]
[![Invite][invite-shield]][invite]
[![Official Discord][discord-shield]][discord-server]
[![License][license-shield]][license]
![Stars][stars-shield]
![Python][python-shield]

슬래시로 작동하는 유틸리티 만능 봇!\
번역, 검색, 날씨와 암호화 기능까지 - [여러 유용한 기능들을 채팅하면서 바로 써보세요][invite]!

## 특징

- 디스코드의 Slash Command 기능 사용으로, `/`만 누르면 모든 명령어가 한번에 나옵니다.
- 번역, 암호화, 날씨 등 실제 채팅할때 유용한 기능들을 담았습니다.
- 가위바위보 등 혼자서 할 수 있는 놀이부터, 2인전이 가능한 틱택토까지!

## 라이선스

WhiteBot의 모든 코드는 GPL v3에 따라 보호됩니다.

## 시작하기

`/도움말` 명령어의 사용으로 기본 명령어의 확인이 가능합니다.

### 유틸리티 명령어

| 명령어  | 설명 |
| ------- | --- |
| `/검색` | 검색어를 검색합니다. 구글, 네이버, 다음, 지식백과, 위키백과, 나무위키의 검색 결과가 표시됩니다. |
| `/전송` | 항목을 임베드 형식으로 전송합니다. 줄바꿈은 적용되지 않습니다. |
| `/암호` | 수신문을 암호화합니다. base16, base32, base64, base85, 아스키 코드로의 변환이 가능합니다. |
| `/해독` | 암호문을 해독합니다. base16, base32, base64, base85, 아스키 코드로부터의 변환이 가능합니다. |
| `/날씨` | 지역의 현재 날씨, 풍향 등을 조회합니다. |
| `/번역` | 수신문을 번역합니다. 한영, 영한, 한일, 일한, 한중, 중한 번역이 지원됩니다. |
| `/투표` | 투표를 시작합니다. |
| `/개표` | 투표를 종료합니다. |
| `/연산` | 유저가 선택한 사칙 연산을 실행합니다. 숫자는 정수, 소수 모두 가능합니다. |
| `/공학계산` | 공학용 계산기 수준의 연산을 제공합니다. |
| `/맞춤법` | 한글 맞춤법을 검사합니다. |
| `/주소단축` | URL을 단축합니다. |
| `/코로나` | 코로나 관련 정보를 출력합니다. |
| `/환율` | 현재 시간 기준 환율로 환전합니다. |

### 관리 명령어

| 명령어    | 설명 |
| --------- | --- |
| `/도움말` | 봇의 도움말을 표시합니다. |
| `/봇`     | 봇의 정보를 전송합니다. 봇의 버전, 업타임 등이 같이 표시됩니다. |
| `/핑`     | 봇의 핑을 전송합니다. |
| `/청소`   | 메시지를 청소합니다. 메시지 관리 권한이 필요합니다. |

### 놀이 명령어

| 명령어        | 설명 |
| ------------ | --- |
| `/가위바위보` | 봇과 가위바위보를 합니다. |
| `/주사위`    | 주사위를 굴립니다. 처음 변수만 사용하였을때는 1부터 A까지, 두번째 변수까지 사용하였을때는 A부터 B까지 굴립니다. |
| `/홀짝`      | 홀짝 게임을 시작합니다. |
| `/틱택토`    | 틱택토(삼목) 게임을 시작합니다. 2인전으로 진행됩니다. |
| `/유튜브`    | 음성 채널에 유튜브 투게더를 활성화시키는 링크를 보냅니다. 음성 채널에 연결되어 있어야 작동하며, 대부분의 서버에서 정상적으로 작동하지 않습니다. |

## 기여하기

WhiteBot에 기여하는 방법에는 여러 가지가 있습니다.

- 버그를 발견하신 경우 [이슈][issues]를 열어주세요.
- 봇에 추가되기를 원하시는 기능도 언제든지 [이슈][issues]로 열어주세요.
- 위 내용들은 [공식 디스코드 서버][discord-server]에서 알려주셔도 무방합니다.

코드에 직접 기여하기를 원하신다면, 먼저 [CONTRIBUTING.md][contributing]를 자세히 읽어주세요.  
코드가 아무리 좋더라도, 가이드라인을 지키지 않으셨다면 PR이 거부될 수 있습니다 :(
