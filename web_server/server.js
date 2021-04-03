const express = require("express")
// const bodyParser = require("body-parser")
//var firebase = require('firebase');
const admin=require('firebase-admin');
const ejs = require('ejs')
var serviceAccount = require('./admin.json');
admin.initializeApp({
credential: admin.credential.cert(serviceAccount),
databaseURL: "https://anti-teft-bike-sih-default-rtdb.firebaseio.com/",
authDomain: "anti-teft-bike-sih-default-rtdb.firebaseapp.com",
});

var db=admin.database();
var db_auth=db.ref("auth");
var db_state=db.ref("state");
const app = express();

app.listen(3000,function (){
  console.log('server is up')
})

app.use(express.json())
app.use(express.static("public"))
app.set('view engine', 'ejs');



function get_auth_information(){
  var data ={}
  db_auth.once('value',function(snap){
    a = JSON.parse(JSON.stringify(snap.val()))
    //console.log(Object.keys(a))
    //console.log(Object.values(a))
    count =0
    for(var i in Object.keys(a)){
      data[Object.keys(a)[count]] = Object.values(a)[count]
      count=count+1
    }
    console.log(data)
    return data
  })

}

function get_state(){
  var data ={}
  db_state.once('value',function(snap){
    a = JSON.parse(JSON.stringify(snap.val()))
    //console.log(Object.keys(a))
    //console.log(Object.values(a))
    count =0
    for(var i in Object.keys(a)){
      data[Object.keys(a)[count]] = Object.values(a)[count]
      count=count+1
    }
    console.log(data)
    return data
  })

}

function lock(){
  var lock_ref = db.ref("auth/lock").set(false, (error) => {
  if (error) {
    // The write failed...
  } else {
    // Data saved successfully!
  }
});

}



app.get("/",function(req,res){
  get_auth_information()
  get_state()
  lock()

  console.log()
  res.send('')
  //console.log(a)



})
