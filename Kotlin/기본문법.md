## Kotlin 기본 문법

코틀린은 **;** 을 사용하지 않고 , 아래와 같이 변수 타입이 뒤에 붙는 형태입니다. (변수 타입을 지정하지 않아도 됩니다)
``` kotlin
val temp: Int = 15
var temp = 15
```

## val , var
코틀린의 있는 2가지 변수 선언 방식입니다.
- val: 변할 수 없는 상수
- var: 일반적인 변수 해당합니다

### val
val은 read-only이면서 로컬 변수가 됩니다. java에선 final에 해당합니다.
>초기화 후에 변할 수 없는 값을 말하게 됩니다.
``` kotlin
val a: Int = 1
val b = 1
val c: Int
c = 100 // 생성자 시점에서 초기화해주지 않아 문법상 오류가 발생하게 됩니다.
```

### var
var은 일반적인 변수에 해당됩니다.
``` kotlin
var x = 1 // x를 Int로 추론할 수 있습니다.
x += 15 

var y: Int = 1 // y를 Int로 고정하였습니다.
y = 15
```
var은 val과 달리 값을 변경할 수 있습니다.
>두 선언 다 타입을 지정하지 않아도 되지만 코드를 짜면서 실수하지 않게 지정하는 것을 추천합니다.

## 함수 생성
자바에서는 함수를 아래와 같이 선언합니다
``` java
public int sum(int a, int b){
    return a + b;
}
```
위의 코드를 코틀린으로 변환시키면 아래와 같이 변하게 됩니다.
``` kotlin
fun sum(a: Int , b: Int): Int {
    return a + b
}
```
자바의 함수 기본 형태
```
int 함수명(변수 타입 변수명) { return값 }
```
을 가지는 반면 Kotlin은
```
fun 함수명(변수명: 변수타입): 반환 타입 {return 값}
```
의 형태를 가집니다.  
여기서 코틀린의 장점은 이 함수를 더 줄일 수 있습니다.
```
// 아래와 같이 Type을 정의하여 return을 정의하거나
fun sum(a: Int, b: Int): Int = a + b
// 또는 아래와 같이 바로 return도 가능합니다.
fun sum(a: Int, b: Int) = a + b
```
한 줄로 표현도 가능합니다. 변수 타입을 명시하거나, 하지 않을 수도 있고 = 을 이용하여 단순히 이 함수가 리턴을 의미하도록 함축적으로 표현 할 수 있습니다.  

함수에 조건식을 추가하게 된다면
``` kotlin
fun sum(a: Int , b: Int): Int {
    if(a>b) return a
    else return b
}
//이 함수를 줄이게 된다면

fun sum(a: Int , b: Int) = if(a>b) a else b
//이렇게 까지 줄일 수 있게 됩니다.
```
## null
코틀린의 기본 변수는 null을 가질 수 없게 되어있습니다.
``` kotlin
var x: Int = 1
x = null // 문법상 오류 발생

var b: Int? = null
b = null // 정상 수행
```
위와 같이 변수 타입 옆에 **?** 을 추가하였을때만 null을 허용하게 됩니다.  

또한 
- nullable:?
- nullable 이면 오류 발생:!!
물음표와 느낌표 두개를 사용하는 경우도 있습니다.  

!!를 붙였을때는 null일 경우 오류가 발생합니다.  

### 함수에서 null의 졍의
```kotlin
// ABC객체의 a를 반환하는 함수에서 만약 abc가 null이라면 null을 반환합니다.
fun abc(abc: ABC?): Int? {
    //...
    return abc?.a
}
```

## Any 사용하기
type을 Any라는 키워드로 작성할 수 있습니다.
``` kotlin
fun getStringLength(obj: Any): Int? {
    if(obj is String){
        //obj는 이떄 자동으로 String으로 변하게 됩니다.
        return obj.length
    }
    // 'obj' is still of type 'Any'
    // Type이 String이 아니라서 null을 return 하게 됩니다.
    return null
}
```
is String이 아님을 나타낼 대는 is앞에 “!” 간단하게 부정할 수 있습니다.
``` kotlin
fun getStringLength(obj: Any): Int? {
    if(!(obj is String)){
        //obj는 이떄 자동으로 String으로 변하게 됩니다.
        return null
    }
    return obj.length
}
```
## loop
코틀린의 loop는 자바와 비슷합니다.
``` kotlin
// Java for
ArrayList<String> arrayList = new ArrayList<>();
for (String s : arrayList) {
    Log.d("TAG", "string : " + s);
}

// Kotlin
val arrayList = ArrayList<String>()
for (s in arrayList) {
    Log.d("TAG", "string : " + s)
}
```

## when
코틀린에는 when이라는 키워드가 있습니다.
when은 if문을 중첩하지 않고 간단하게 Any와 함께 구현할 수 있습니다.
``` kotlin
fun main(args: Array<String>) {
    cases("Hello") // String
    cases(1) // Int
    cases(System.currentTimeMillis()) // Long
    cases(MyClass()) // Not a string
    cases("hello") // Unknown
}

fun cases(obj: Any) {
    when (obj) {
        1 -> println("One")
        "Hello" -> println("Greeting")
        is Long -> println("Long")
        !is String -> println("Not a string")
        else -> println("Unknown")
    }
}
```
위의 예제에 결과값입니다.
```
Greeting
One
Long
Not a string
Unknown
```
## ranges
숫자의 범위를 지정하여 사용하는 방법입니다.
``` kotlin
for (i in 1..5) {
    // 1부터 5까지 반복하는 반복문
    println(x)
}
```
Kotlin에서는 ranges 형태를 if문에서도 사용할 수 있습니다.
``` kotlin
val array = arrayList<String>
array.add("aaa")
array.add("bbb")

val x = 3

if (x !in 0..array.size - 1)
  println("Out: array 사이즈는 ${array.size} 요청한 x = ${x}")

//위의 출력 값은
// Out: array 사이즈는 2 요청한 x = 3
```

## 마무리
처음 접하는 코틀린 언어 기본문법을 다뤄봤는데 여러언어에서 봤던것들이 많아서 익히기 생각보다 익히기 편한거 같습니다 즐거운 코틀린 하셨으면 좋겠습니다!
