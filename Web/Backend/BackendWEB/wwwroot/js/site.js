// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.


function sendFile(){
    
}

function printGistogram(){
    var height = 500,
        width = 500,
        margin=30,
        padding = 2,
        data = [{x: 1, y: 55},
            {x: 2, y: 67}, {x: 3, y: 74},{x: 4, y: 63},
            {x: 5, y: 56}, {x: 6, y: 24}, {x: 7, y: 26},
            {x:8, y: 19}, {x: 9, y: 42}, {x: 10, y: 88},
            {x: 11, y: 80}, {x: 12, y: 77}
        ];

    var svg = d3.select("body").append("svg")
        .attr("class", "axis")
        .attr("width", width)
        .attr("height", height);

// длина оси X= ширина контейнера svg - отступ слева и справа
    var xAxisLength = width - 2 * margin;

// длина оси Y = высота контейнера svg - отступ сверху и снизу
    var yAxisLength = height - 2 * margin;

// функция интерполяции значений на ось Х  
    var scaleX = d3.scale.linear()
        .domain([1, 13])
        .range([0, xAxisLength]);

// функция интерполяции значений на ось Y
    var scaleY = d3.scale.linear()
        .domain([100, 0])
        .range([0, yAxisLength]);

// создаем ось X   
    var xAxis = d3.svg.axis()
        .scale(scaleX)
        .orient("bottom");
// создаем ось Y             
    var yAxis = d3.svg.axis()
        .scale(scaleY)
        .orient("left");

    // отрисовка оси Х             
    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform",  // сдвиг оси вниз и вправо
            "translate(" + margin + "," + (height - margin) + ")")
        .call(xAxis);

    // отрисовка оси Y 
    svg.append("g")
        .attr("class", "y-axis")
        .attr("transform", // сдвиг оси вниз и вправо на margin
            "translate(" + margin + "," + margin + ")")
        .call(yAxis);

// рисуем горизонтальные линии 
    d3.selectAll("g.y-axis g.tick")
        .append("line")
        .classed("grid-line", true)
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", xAxisLength)
        .attr("y2", 0);
// создаем объект g для прямоугольников
    var g =svg.append("g")
        .attr("class", "body")
        .attr("transform",  // сдвиг объекта вправо
            "translate(" + margin + ", 0 )");
// связываем данные с прямоугольниками
    g.selectAll("rect.bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar");
// устанавливаем параметры прямоугольников
    g.selectAll("rect.bar")
        .data(data)
        .attr("x", function (d) {
            return scaleX(d.x);
        })
        .attr("y", function (d) {
            return scaleY(d.y) + margin;
        })
        .attr("height", function (d) {
            return yAxisLength - scaleY(d.y);
        })
        .attr("width", function(d){

            return Math.floor(xAxisLength / data.length) - padding;
        });

    g
        .append("line")
        .attr("x1", scaleX(data[9].x) - padding)
        .attr("y1", scaleY(data[9].y) + margin)
        .attr("x2", scaleX(data[10].x) - padding)
        .attr("y2",  scaleY(data[10].y) + margin)
        .style("stroke", "red")
        .style("stroke-width", 3);

    g
        .append("line")
        .attr("x1", scaleX(data[10].x) - padding)
        .attr("y1", scaleY(data[9].y) + margin)
        .attr("x2", scaleX(data[9].x) + padding)
        .attr("y2", scaleY(0) + margin)
        .style("stroke", "red")
        .style("stroke-width", 3);
}