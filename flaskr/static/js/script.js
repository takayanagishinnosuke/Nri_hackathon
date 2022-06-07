//canvasの取得
let ctx = document.getElementById('radar-chart');
let enctx = document.getElementById('en-chart');


//valudate取得用
let date = []
//残高val取得用
let balance = []
//入出金val取得用
let transactionType_one = []
let transactionType_two = []

//jsonをobjに変換
let json_str = JSON.stringify(api_data)

let json_count_obj = JSON.parse(js_count)
let json_obj = JSON.parse(json_str)

//jsonのkeyの数を取得
let key = Object.keys(json_obj)

//json確認用
console.log(json_obj) //api_jsonデータ
console.log(json_count_obj) //家族毎の却下押下カウントデータ

//valudate取得
for (let i in key){
  i = i++
  date.push(json_obj[i]["valueDate"])
  balance.push(json_obj[i]["balance"])
  if (json_obj[i]["transactionType"] == 1){
    transactionType_one.push(json_obj[i]["transactionType"])
  }else{
    transactionType_two.push(json_obj[i]["transactionType"])
  }
}

let Ttype_len_one = transactionType_one.length
let Ttype_len_two = transactionType_two.length


//折れ線チャート作成
let data = {
  labels:date,
  datasets:[{
    label:'残高',
    data:balance,
    borderColor: 'rgba(4,194,172,2)',
    lineTension:0,
    fill:false,
    borderWidth:3
  }]
};

let option ={
  scales:{
    xAxes:[{
      scaleLabel:{
        display:true,
        labelString:'年月日'
      }
    }],
    yAxes:[{
      ticks:{
        min:0,
        userCallback:function(tick){
          return tick.toString() + '円';
        }
      },
      scaleLabel:{
        display:true,
        labelString:'残高'
      }
    }]
  },
  title:{
    display:true,
    text:'口座残高推移'
  }
};
//折れ線チャートをcanvasにセット
let myRadarChart = new Chart(ctx,{
  type:'line',
  data:data,
  options:option
});

//円グラフ作成
let endata = {
  labels:['入金','出金'],
  datasets:[{
    backgroundColor: ["#00ff7f", "#fa8072"],
    data:[Ttype_len_one,Ttype_len_two]
  }]
}

let enoptions = {
  responsive:false,
  title:{
    display:true,
    text:'入出金比率'
  }
}

//円グラフをcanvasにセット
let myEnChart = new Chart(enctx,{
  type:'doughnut',
  data:endata,
  options:enoptions
});