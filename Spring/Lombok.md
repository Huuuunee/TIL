## LomBok이란?

`Lombok`이란 Java의 라이브러리로 반복되는 메소드를 `Annotation`을 사용해서 자동으로 작성해주는 라이브러입니다.  
 보통 DTO나 Model, Entity의 경우 여러 속성이 존재하고 이들이 가지는 프로퍼티에 대해서 Getter나 Setter, 생성자 등을 매번 작성해줘야 하는 경우가 많은데 이러한 부분을 자동으로 만들어주는 라이브러리라고 할 수 있습니다.

Lombok을 이용해서 작성한 코드는 컴파일 과정에서 **Annootation**을 이용해서 코드를 생성하고 이런 결과물이 .class에 담기게 됩니다.

## LomBok의 장점

어노테이션 기반의 코드 자동생성을 통한 생산성 향상  
반복코드 다이어트를 통해 가독성 및 유지보수성 향상  
Getter/Setter 외 빌더 패턴이나 로그생성 등 다양한 방면으로 활용 가능

## LomBok의 단점

롬복의 @Data 어노테이션이나 @toString 어노케이션으로 자동 생성되는 toString()메서드는 순환 참조 또는 무한재귀호출 문제로 인해 StackOverflowError가 발생할 수도 있다.  
물론 이 문제를 인지한 롬복에서 해결할 수 있는 속성을 제공하지만 롬복이 편리하다는 이유만으로 마구 사용한다면 여러가지 예외문제가 발생할 수 있음을 인지해야 한다.

## LomBok과 일반 Java의 코드 차이

멤버라는 모델 클래스가 있다하면  
ex)

```java
public class Member{
    private String name;

    private String password;

    private Integer age;

    public String getName() {
        return name;
    }

    public void setName(String name){
        this.name = name;
    }
     public String getPassword() {
        return password;
    }

    public void setPassword(String password){
        this.password = password;
    }
     public Integer getAge() {
        return age;
    }

    public void setAge(Integer age){
        this.age = age;
    }
}
```

위 코드를 Lombok을 이용하면 다음과 같이 축소할 수 있다.  
클래스에 @Getter, @ToString 등의 어노테이션을 붙여주기만 하면 된다.

```java
import lombok.*;

@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class Member{
    private String name;

    private String password;

    private Integer age;
}
```

또는 이 다섯개의 어노테이션을 @Data 어노케이션 하나만 붙여 사용할 수도 있다.

**\*데이터 어노테이션.**
@Data 어노테이션을 활용하면 @ToString, @EqualsAndHashCode, @Getter, @Setter, @RequiredArgsConstructor를 자동완성 시켜준다.

ex)

```java
import lombok.*;

@Data
public class Member{
    private String name;

    private String password;

    private Integer age;
}
```

이것만 봐도 코드가 엄청나게 줄어들었다!

**로그 관련 어노테이션**
@Log4j2와 같은 어노테이션을 활용하면 해당 클래스의 로그 클래스를 자동 완성 시켜준다.

ex)

```java
@RestController
@RequestMapping(value = "/log")
@Log4j2 public class LogController {
    @GetMapping(value = "/log4j2")
        private ResponseEntity log() { 
            log.error("Error"); 
        return ResponseEntity.ok().build(); 
            } 
        }
```
잘사용하면 좋은 LomBok 남발하지 말고 잘사용합시다 😉