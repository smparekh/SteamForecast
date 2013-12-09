 var days = [];
 var dayData = []
 for (var i = 1; i <= 36; i++)
 {
     days.push(i.toString());
     dayData.push(i*2);
 }
      
 var data = {
      labels : days,
      datasets : [
      {
          fillColor : "rgba(151,187,205,0.5)",
          strokeColor : "rgba(151,187,205,1)",
          pointColor : "rgba(151,187,205,1)",
          pointStrokeColor : "#fff",
          data : dayData
      }
      ]
}
var ctx = document.getElementById("exampleChart").getContext("2d");
new Chart(ctx).Line(data); 
