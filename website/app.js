import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
// import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js";
import {getFirestore , collection, getDocs} from "https://www.gstatic.com/firebasejs/9.10.0/firebase-firestore.js"
google.charts.load("current", { packages: ["corechart"] });
// TODO: Add SDKs for Firebase products that you want to use
const firebaseConfig = {
  apiKey: "AIzaSyBSSIPd1VkpAN3lZjSjvUdgPN_-8uEK_MY",
  authDomain: "pythoncar-a08c8.firebaseapp.com",
  projectId: "pythoncar-a08c8",
  storageBucket: "pythoncar-a08c8.appspot.com",
  messagingSenderId: "474695943595",
  appId: "1:474695943595:web:2cda4327a4a96196c83eee",
  measurementId: "G-G73TVMV8SR",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const db = getFirestore(app)
const table = document.getElementById('table')
const toggleEl = document.getElementById('toggle');

// const  dgh = document.getElementById('demo').innerHTML="BEN"
// document.getElementById("demo").style.color = "red";
let carount = document.getElementById('carcount')
let motorcount = document.getElementById('carcount1');
let buscount = document.getElementById('carcount2');
let truckcount = document.getElementById('carcount3');
let carTotal = document.getElementById('carcount4');


var numcar = 0;
var nummotor = 0;
var numbus = 0;
var numtruck = 0;
var totalCar = 0


async function getProjectCar(db){
    const proCol  = collection(db,'project')
    const proSnapshot = await getDocs(proCol)
    return proSnapshot
}

function showData(projectCar){
    // console.log(projectCar.data())
    const row = table.insertRow(-1)
    const date = row.insertCell(0)
    const time_start = row.insertCell(1)
    const time_stop = row.insertCell(2)
    const car = row.insertCell(3)
    const motor = row.insertCell(4)
    const bus = row.insertCell(5)
    const truck = row.insertCell(6)
    const total = row.insertCell(7)
    date.innerHTML  = projectCar.data().date
    time_start.innerHTML = projectCar.data().time_start
    time_stop.innerHTML  = projectCar.data().time_stop
    car.innerHTML = projectCar.data().Car
    motor.innerHTML = projectCar.data().Motorcycle
    bus.innerHTML = projectCar.data().Bus
    truck.innerHTML = projectCar.data().Truck
    total.innerHTML = projectCar.data().Total
}

function showDasborad(projectCar){
    var carnum = parseInt(projectCar.data().Car)
    var motornum = parseInt(projectCar.data().Motorcycle)
    var busnum = parseInt(projectCar.data().Bus)
    var trucknum = parseInt(projectCar.data().Truck)
    var totalnum = parseInt(projectCar.data().Total)
    numcar = numcar+carnum
    carount.innerHTML = "จํานวณ "+numcar+ " คัน"
    nummotor = nummotor + motornum
    motorcount.innerHTML = "จํานวณ "+nummotor+ " คัน"
    numbus = numbus + busnum
    buscount.innerHTML = "จํานวณ "+numbus+ " คัน"
    numtruck +=  trucknum
    truckcount.innerHTML  = "จํานวณ "+numtruck+ " คัน"
    totalCar += totalnum
    carTotal.innerHTML = "จํานวณ "+totalCar+ " คัน"
}
// console.log(caunum);



// ดึงกลุ่ม document
const data01 = await getProjectCar(db)
// data01.forEach(projectCar => {
//     showData(projectCar)
//     showDasborad(projectCar)
// });

toggleEl.addEventListener('click',()=>{
    // console.log("555");
    document.body.classList.toggle('show-nav');
});

function ShowData01(){
    data01.forEach(projectCar => {
        showData(projectCar)
        showDasborad(projectCar)
    });
}

    let minDate, maxDate;
 
// Custom filtering function which will search data in column four between two values
        $.fn.dataTable.ext.search.push(
            function( settings, data, dataIndex ) {
                let min = minDate.val();
                let max = maxDate.val();
                let date = new Date( data[0] );
        
                if (
                    ( min === null && max === null ) ||
                    ( min === null && date <= max ) ||
                    ( min <= date   && max === null ) ||
                    ( min <= date   && date <= max )
                ) {
                    return true;
                }
                return false;
            }
        );
    
    $(document).ready(function () {
        
        minDate = new DateTime($('#min'), {
            format: 'DD-MM-YYYY'
        });
        maxDate = new DateTime($('#max'), {
            format: 'DD-MM-YYYY'
        });
        let table = $('#table').DataTable({
            "paging": true,
            "lengthChange": true,
            "searching": true,
            "ordering": true,
            "info": true,
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.13.1/i18n/th.json"
            },
            columnDefs: [
                // Center align the header content of column 1
               { className: "dt-head-center", targets: [ 0,1,2,3,4,5,6,7 ] },
            ]
        });
        // $('#min, #max').on('change', function () {
        //     table.draw();
        // });
        $('#btnSU').click(function(){
            table.draw();
        });
    });

ShowData01();


const data = {
  labels: ['รถยนต์', 'รถจักรยานยนต์', 'รถบัส', 'รถบรรทุกสินค้า'],
  datasets: [{
      label: 'จํานวณ',
      data: [numcar,nummotor , numbus, numtruck],
      backgroundColor: [
          'rgba(255, 99, 132)',
          'rgba(54, 162, 235)',
          'rgba(255, 206, 86)',
          'rgba(75, 192, 192)',
      ],
      borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
      ],
      borderWidth: 3
  }]
}


const datapie = {
  labels: ['รถยนต์', 'รถจักรยานยนต์', 'รถบัส', 'รถบรรทุกสินค้า'],
  datasets: [{
      label: 'จํานวณ',
      data: [numcar,nummotor , numbus, numtruck],
      backgroundColor: [
          'rgba(255, 99, 132)',
          'rgba(54, 162, 235)',
          'rgba(255, 206, 86)',
          'rgba(75, 192, 192)',
      ],
      borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
      ],
      hoverOffset: 5
  }]
}

const config = {
  type: 'bar',
  data,
  options: {
      scales: {
          y: {
              beginAtZero: true
          }
      }
  }
}

const myChart01 = new Chart(
  document.getElementById('myChart'),
  config,
);

const configpie = {
  type: 'doughnut',
  data: datapie,
  options: {
      scales: {
          y: {
              beginAtZero: true
          }
      }
  }
}

const myChartpie = new Chart(
  document.getElementById('myChartpie'),
  configpie,
);


