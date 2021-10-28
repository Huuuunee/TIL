var button = document.getElementById('button');
var input = document.getElementById('input');
var list = document.getElementById('list');

button.addEventListener('click',clickButton);

var cnt = 1;

function clickButton() {
  var temp = document.createElement('li');
  temp.setAttribute("class", "list-group-item");
  temp.setAttribute("id", "li"+cnt);
  temp.innerHTML = input.value;
  temp.innerHTML += "<button style='float: right;' class='btn btn-outline-secondary' type='button' onclick='remove("+cnt+")'>삭제</button>";
  list.appendChild(temp);
  cnt++;
}
function remove(cnt) {
  var li = document.getElementById('li'+cnt);
  list.removeChild(li);
}

window.onload=function today(){
  let today = new Date();   

  let year = today.getFullYear(); // 년도
  let month = today.getMonth() + 1;  // 월
  let date = today.getDate();  // 날짜
  let day = today.getDay();  // 요일

//document.write(year + '/' + month + '/' + date)
//document.write('<br>')
//document.write(day);
document.getElementById("dong").textContent = new Date();
}
function today1(){
  let today = new Date();   

  let year = today.getFullYear(); // 년도
  let month = today.getMonth() + 1;  // 월
  let date = today.getDate();  // 날짜
  let day = today.getDay();  // 요일

//document.write(year + '/' + month + '/' + date)
//document.write('<br>')
//document.write(day);
document.getElementById("dong").textContent = new Date();
}
