const express = require('express');
const app = express();
const mysql = require('mysql2');
const crypto = require('crypto');
const { off } = require('process');
const hostname = '10.120.74.60';
const port = 3000;
const pool = mysql.createPool({ // DB 연결 설정
  host: 'localhost',
  user: 'root',
  port: '3306',
  password: 'ksh1004@',
  connectionLimit: 10,
  database: 'db_test'
});

app.use(express.json())
app.use(express.urlencoded({ extended: false }));

pool.getConnection((err, conn) => { // DB 연결
  if (!err) {
    console.log("Database is connected ... \n\n");
  } else {
    console.log("Error connecting database ... \n\n");
  }
});

app.post('/register', (req, res) => {
  const saltRounds = 10;
  const param = [req.body.email, req.body.id, req.body.password]
  console.log("who get in here/login");
  pool.query('INSERT INTO login(`email`,`id`,`password`) VALUES (?,?,?)', param, (err, rows, field) => {
    if (err)
      console.log(err);
  })
  res.end()
})


app.get('/login', (req, res) => {

  console.log(test);
  console.log("who get in here/login");
  console.log(req.body);
  pool.query(every, (err, rows, field) => {
    res.send(test)
  });

});

app.post('/login', (req, res) => {
  const id = req.body.id; // 'hi'
  const ps = req.body.password; // 'ada'
  const email = req.body.email;
  console.log(req.body); // {id:'hi', password:'ada'}
  const test_query = 'SELECT * FROM login WHERE id=?'; // hi, tedw , test == 'hi'

  pool.query(test_query, [email, id, ps], (err, rows, field) => {
    if (err) {
      res.status(500).send('서버오류인데 어쩔건데');
    }
    console.log(id);
    console.log(email);
    console.log(ps);
    console.log(rows[0].email);

    if (rows[0]) {
      res.send('어랍쇼 아이디가 없는데요?');
    }

    else if (rows[0]) {
      crypto.pbkdf2(rows[0].password, ps, 100000, 64, 'sha512', function (err, derivedKey) {
        const hash = derivedKey.toString('hex')
        if (err)
          console.log(err);
        else if (rows[0].password === ps) {
          return res.send('어 회원가입하셧군요 좋아요');
        }
        else if (rows[0].password != ps) {
          return res.send('비밀번호 틀려써!');
        }
      });
    }
  });
});


app.listen(port, hostname, () => { // 서버 대기만드는 구문
  console.log(`서버 켜졌어! ${port}`)
})
