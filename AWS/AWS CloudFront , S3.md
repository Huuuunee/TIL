서버리스 웹 호스팅과 CloudFront로 웹 가속화 구성하기
=====
아키텍쳐에 구현할 기술 : 서버가 없어도 구성이 가능한 정적 웹 호스팅을 만들고, 웹 속도를 높일수 있는 콘텐츠 전송 네트워크 서비스를 연동할겁니다!<br>
여기서 위 기술을 구현할때 필요한 AWS서비스는 Amazon S3,Amazon CloudFront라는 것과 간단한 HTML 파일 또는 소스가 필요합니다!<br><br>

Amazon CloudFront랑 Amazon S3가 무엇인가?<br>
----------
S3 Bucket안에 HTML,그림,동영상 파일 등 컨텐츠들을 업로드하면 웹 호스팅 설정을 하면 웹사이트처럼 작동할수있도록 구성할수있습니다.<br>
기본적으로 S3는 인터넷용 스토리지이고 웹 서비스 인터페이스를 사용해서 웹에서나 어디서나 원하는 양의 데이터를 저장,검색이 가능해서 S3 자체만으로도 웹 호스팅이 가능합니다 이것이 바로 객체 스토리지 서비스의 특징이라 할수있습니다 하지만 여기서 웹에서 불러올 파일들이 크면 클수록 로딩속도가 지연되는데 이것을 해결할 수 있는 것이 바로 Amazon CloudFront라는 서비스입니다!.
<br>

아키텍쳐 구현 순서
----
S3정적 웹 호스팅 구성하기<br>
<li>S3 Bucket 생성
<li>정적 웹 사이트 호스팅 활성화
<li>웹 사이트 엔드포인트 테스트

CloudFront를 이용해 웹사이트 속도 높이기<br>
<li>CloudFront 배포 만들기
<li>생성된 CloudFront 도메인 확인

<br>
  
S3 버킷 만들기
====
  
1.AWS사이트에서 S3접속하기.
----
  
![1](https://user-images.githubusercontent.com/81404026/136945870-0bd9455a-a6f4-49d0-96c5-cdea60ef046b.png)
<br>
2.버킷 만들기 누르기
----
  
여기서 버킷이름은 조건이 있습니다.
  
![3](https://user-images.githubusercontent.com/81404026/136945875-c13ae8f0-ba98-4ea5-8baa-48d7330f5267.png)
위 규칙들을 지켜서 만들어야 합니다!
  
![2](https://user-images.githubusercontent.com/81404026/136945873-9a2232f8-da1c-4fa5-9bcb-d6f40cfbd15f.png)

설정방법
====
  
AWS 리전
----
  
리전은 자신이 원하는 리전을 선택하면 되요! 전 한국에서 가장 가까운 서울 리전을 택했어요.
<br><br>

액세스 차단 설정
----
  
아래로 내리면 액세스 차단 설정이란것이 있는데 S3는 외부 인터넷이 접속 가능한 대용량 객체 스토리지이기 때문에 보안기능 설정이 필요해요 여기서 저희는 모든 인터넷을 허용하고 사용해볼것이기 때문에 체크되있는 부분을 해제 해주시면 되요😄
<br><br>

Bucket 파일 업로드하기
----
버킷을 만들고 나면 정적 웹 사이트 호스팅이란 옵션을 켜줘야 하는데 S3에 들어가서 속성을 누르고 아래로 내리면 옵션이 떠요 여기서 편집을 누르고 활성화 시켜주고 변경사항 저장누르기!.
(인덱스 문서는 index.html이라 작성해주시면 되요)
![4](https://user-images.githubusercontent.com/81404026/136945877-f0061cf1-7bb7-4230-a7f5-345611617e3b.png)
<br>
이제 버킷 정책을 편집해줘야 하니 관리를 눌러서 버킷 정책 편집을 눌러 들어가줘요
![5](https://user-images.githubusercontent.com/81404026/136945878-b1268fa0-7cc3-4510-9c17-74290ae55cee.png)
여기서 정책 생성기를 눌러서 들어가기전 버킷 ARN을 복사해주세요! 정책 생성기를 들어가면 <br>

<li>Select Type of Policy는 S3 Bucket Policy로 설정해줘요
<li>Principal은 *로 써주세요
<li>Action는 체크박스를 선택하여 주세요(All Actions)
<li>Amazon Resource Name (ARN)은 아까 복사해논 버킷ARN을 붙여놓고 Add Statement 클릭!
<br>
<br> 
그러면 이제 아래 Generate Policy라는 버튼이 나와요!이 버튼을 클릭해주세요
클릭하면 아래 화면이 나올텐데 안에 있는 코드들을 복사해서 버킷 정책에다가 붙여놔주세요!

![6](https://user-images.githubusercontent.com/81404026/136945879-da85d350-1258-4a37-ad6a-f5e9384ce9ae.png)

붙이고 나서 resourse 마지막 부분에 "/*" 를 입력하고 변경사항 저장을 눌러주세요.

그러면 이제 내 S3 버킷에다가 파일을 업로드해볼까요?<br>
파일을 이렇게 업로드하고

![7](https://user-images.githubusercontent.com/81404026/136945880-e5cfef02-f30d-43b9-95c0-0c896d299ca1.png)내가 원하는 파일의 url을 복사해서 웹에 붙여넣기 하면

![8](https://user-images.githubusercontent.com/81404026/136945881-3b3e7ee0-6fcd-4338-8d2d-811b6add4fb9.png)이렇게 정상적으로 열리는걸 볼수 있어요!

CloudFront 설정하기
====
AWS CloudFront를 접속후 배포 생성을 눌러서 원본도메인을 선택하면 내가 만들어논 S3가 제일 위에 뜰거에요! 이걸 선택해주시고 다른것들은 기본값으로 하고 배포생성을 해주시면 되요.
![9](https://user-images.githubusercontent.com/81404026/136945883-e650e21e-7837-4244-bf24-98d9acb7782a.png)
이제 이 화면에서 배포 도메인 이름을 복사해준뒤 내 Html 파일로 가서 이미지 경로란에 적어주도록 할게요
  
  
<div align="center">
  <img src="https://user-images.githubusercontent.com/81404026/136945885-165ba377-8aa1-42d4-9cf8-65abd71fbbec.png" />
</div>
 
  
  <br>
이제 이 파일을 버킷에 올리고 url로 접속하면!
 
![11](https://user-images.githubusercontent.com/81404026/136945887-18fb7c56-7321-4157-8be0-29ae9d1b8b4f.png)
 
 이렇게 잘 적용된 모습을 볼 수 있습니다!
<br>

내가 캐싱된 파일을 불러왔는지 확인하는 방법은 크롬 개발자 도구를 누른후 Network를 누르고 F5를 누르면 확인하실수 있으십니다.
![12](https://user-images.githubusercontent.com/81404026/136945892-a9cc79d5-bb7f-483d-ae8c-cfe6aa399b14.png)
