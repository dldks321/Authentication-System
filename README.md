# SGW-Authentication-System
Smilegate Winter Dev Camp 2022 Personal Assignment

- Project outline(프로젝트에 대한 개요)

This is a project to implement a Authentication system, which is a personal project for the 2nd Smilegate Winter Dev Camp.\
The language used Python, and the main usage framework is Django and FastAPI.\
The front-end and back-end were developed separately into different virtual environments, and the libraries and frameworks used for each virtual environment are stored in requirements.txt.

스마일게이트 윈터데브캠프 2기 개인프로젝트인 인증시스템 구현 프로젝트입니다.\
언어는 파이썬을 사용하였으며, 주 사용 프레임워크는 Django와 FastAPI입니다.\
프론트엔드, 백엔드는 각자 다른 가상환경으로 나누어서 개발했으며, 각 가상환경에 사용된 라이브러리와 프레임워크는 requirements.txt에 저장되어 있습니다.

- Technology stack(기술 스택)

The technology stack for the project is as follows:

해당 프로젝트의 기술 스택은 다음과 같습니다.

![구성도 drawio (1)](https://user-images.githubusercontent.com/80047618/209529771-250b04e9-344f-4ac3-beb6-5a00c3595b44.png)

- Project progress(프로젝트 진행상황)

<Requirement(필수조건)>
1. Registration, Login Page(가입, 로그인 페이지) [Complete(완료)]
2. User Management Page(유저 관리 페이지) [Complete(완료)]
3. Authentication Server API(인증 서버 API) [Complete(완료)]
4. Using RDBMS(RDBMS 사용) [Complete(완료)]
5. Password Encryption(비밀번호 암호화) [Complete(완료)]

<Additional requirement(선택조건)>
1. Cache(캐시) [Uncomplete(미완료)]
2. E-Mail Authentication(E-Mail 인증) [Progress(진행중)]
3. Change Password(비밀번호 변경) [Progress(진행중)]

\
\
\

해당 문서 아랫부분은 코드리뷰를 위한 것으로 영번역이 없음.

The bottom part of the document is for code review and there is no English translation.


- 코드중 확인받고 싶은 부분

백엔드 부분에서는 성능개선 방안, 보안성 강화에 대한 피드백을 받고싶습니다.\
프론트 부분에서는 서버에 집중하고 싶어 간략하게 작업하다보니 피드백을 받는다면 전체적으로 받아야 될 듯 합니다.\


- 개발관련 과정에서 궁금했던 부분

1. 패스워드 해싱에 관한 알고리즘을 찾아보니, KISA의 기준으로는 SHA계열의 알고리즘을 사용할 것을 권고하나, SHA 라이브러리 설명문서나 외국계열 문서에서는 bcrypt나 Argon2 계열의 알고리즘을 사용할 것을 권장하고 있습니다. 이 상황의 경우, 어느 기준을 따르는 것이 맞습니까?
2. 유저 관리 페이지에서 필요한 상호작용(유저정보 확인, 유저정보 변경, 유저 삭제 등)의 작업을 인증API에 작업하다 보니 생각난 질문입니다.\
유저관리에 대한 기능들은 API에서 분리를 하는 것이 좋습니까? 아니면 인증API에 기능을 몰아 넣는 것이 맞나요? 아니면 해당 페이지에서 직접적으로 유저 Database에 접근하는 것을 허용하는 방안에 대해서는 어떻게 생각하시는지 궁금합니다.
