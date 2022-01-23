# [JS] 자바스크립트 기본 문법

**JS실력 향상하기**  
  
처음부터 시작하는 JS기본 문법  

### console.log()
~~~
콘솔 창에 출력할때 사용한다 C에 print()대신 써서 값을 확인하기 좋다 자주 쓰기.
~~~

## 선언
C에선 int,float,string을 사용했지만 JS에선 이름 앞에 let,const를 사용하여 변수/상수를 선언 해줘야 한다.
  
  
### let (변수선언)
~~~
변수를 선언할때 사용한다 선언하고 나서 값을 변경할 수 있다(mutable).  
var는 hoisting현상이 있어서 잘 사용하지 않는다.
~~~

### const (상수선언)
~~~
상수를 선언할 때 사용한다,한번 선언하면 값을 변경할 수 없다(immutable).
~~~
  
## 기본 내장함수

### split()
~~~ js
문자열을 쪼개어 배열에 담아준다.

let name = "sihun";
name.split('');  //['s','i','h','u','n']

let time = "12:30";
time.split(':'); //['12','30']

let num = '01012341234';
const num_list = num.split('');
num_list[2] = '1';
num_list.join(''); //'01112341234'
~~~

### join()
~~~ js
배열의 원소들을 하나의 문자열로 만들어준다. array.join('구분할 것')

const array = ['나','는','바보'];
array.join(''); //'나는바보'
array.join(' '); //'나 는 바보'
~~~

### toString()
~~~ js
숫자를 문자열로 바꿔준다

let num = 123;
const num_string = num.toString(); //'123'
~~~

### Number()
~~~ js
문자를 숫자로 바꿔준다

let num = '123';
const num_hello = Number(num); //123
~~~

### parseInt()
~~~ js
문자열을 정수로 만들어준다

let num_string = '123';
const num = parseInt(num_string);
~~~

### isNaN()
~~~ js
숫자인지 아닌지 검사하는 함수 숫자면 false 숫자가 아니면 true를 반환한다

let num = 123;
const result = isNaN(num); //false
~~~

## 조건문과 반복문
배열이나 문자열을 돌면서 연산을 수행하거나 비교할 때 사용한다

### for문
~~~ js
for(let 초기값; 조건(끝); 구문실행){실행시킬 연산들}

for (let i = 0;i< array.length;i++){

}

for (let data of dataList){

}
~~~
### if else문
~~~ js
if (조건1){
    statement1
}else if (조건2){
    statement2
}

if(조건1){
    statement1
}else {
    statement2
}
~~~

### switch
~~~ js
조건식에서 비교할 값이 많을 때 쓰기 좋다

switch (조건) {
    case 값1:
        statement1;
        break;
    case 값2:
        statement2;
        break;
    ...
    default:
        statement3; //맞는 값이 없다면
}
~~~

### while 문
~~~js
while (i<10)
{
    statment
    i++
}
~~~

## 연산자

### 논리 연산자

**&& (AND)**  
**|| (OR)**

### 비교 연산자

**===/!==** 타입까지 검사

**==/!=** 타입은 보지 않는다.

### 삼향 연산자
`조건 ? 'yes' : 'no'`