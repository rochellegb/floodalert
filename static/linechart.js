var margin = {top: 10, right: 30, bottom: 60, left: 60},
    width = 750 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("#linechart")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

$( function() {
    $( "#datepicker" ).datepicker();
  } );

$('#Day').click(function (){
    let date_picker = $('#datepicker').val();
    $.ajax({
        url: '/day',
        method: 'get',
        data: { "date": date_picker},
        success:  function(d){
            svg.selectAll("*").remove();
            const val = $('#Day').text();
            $("#dropdownMenuButton").text(val)
            const data = d.map(function(i) {
                return { hour: Number(i.hour), height : i.height };
                });

            var x = d3.scaleLinear()
                .domain([0, 24])
                .range([ 0, width ]);

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x).ticks(24));

            svg.append("text")
                .attr("class", "x label")
                .style("text-anchor", "middle")
                .attr("x", width - 300)
                .attr("y", height + 40)
                .text("Hours");

            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return d.height; })])
                .range([ height, 0 ]);

            svg.append("g")
                .call(d3.axisLeft(y));

            svg.append("g")
                .selectAll("dot")
                .data(data)
                .enter()
                .append("circle")
                    .attr("cx", function(d) { return x(d.hour) } )
                    .attr("cy", function(d) { return y(d.height) } )
                    .attr("r", 4)
                    .attr("fill", "#69b3a2")

            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 2.5)
                .attr("d", d3.line()
                .x(function(d) { return x(d.hour) })
                .y(function(d) { return y(d.height) }));
        },
        error: function(xhr) {
            alert("error")
        }
    });
});

$('#Month').click(function () {
    let date_picker = $('#datepicker').val();
    $.ajax({
        url: '/month',
        method: 'get',
        data: {'date': date_picker } ,
        success: function(d){
            svg.selectAll("*").remove();
            const val = $('#Month').text();
            $("#dropdownMenuButton").text(val)
            const data = d.map(function(i) {
                return { day: Number(i.day), height : i.height };
                });

            var x = d3.scaleLinear()
                .domain([0, 31])
                .range([ 0, width ]);

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x).ticks(31));

            svg.append("text")
                .attr("class", "x label")
                .style("text-anchor", "middle")
                .attr("x", width - 300)
                .attr("y", height + 40)
                .text("Days");

            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return d.height; })])
                .range([ height, 0 ]);

            svg.append("g")
                .call(d3.axisLeft(y));

            svg.append("g")
                .selectAll("dot")
                .data(data)
                .enter()
                .append("circle")
                    .attr("cx", function(d) { return x(d.day) } )
                    .attr("cy", function(d) { return y(d.height) } )
                    .attr("r", 4)
                    .attr("fill", "#69b3a2")

            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 2.5)
                .attr("d", d3.line()
                .x(function(d) { return x(d.day) })
                .y(function(d) { return y(d.height) }));
         },
         error: function(xhr){
            alert('Please enter valid date')
         }
    });
});

$('#Year').click(function(){
    let date_picker = $('#datepicker').val();
    $.ajax({
        url: '/year',
        method: 'get',
        data: {'date': date_picker},
        success: function(d){
            svg.selectAll("*").remove();
            const val = $('#Year').text();
            $("#dropdownMenuButton").text(val)
            const data = d.map(function(i) {
                return { month: Number(i.month), height : i.height };
                });

            var x = d3.scaleLinear()
                .domain([0, 12])
                .range([ 0, width ]);

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            svg.append("text")
                .attr("class", "x label")
                .style("text-anchor", "middle")
                .attr("x", width - 300)
                .attr("y", height + 40)
                .text("Months");

            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return d.height; })])
                .range([ height, 0 ]);

            svg.append("g")
                .call(d3.axisLeft(y));

            svg.append("g")
                .selectAll("dot")
                .data(data)
                .enter()
                .append("circle")
                    .attr("cx", function(d) { return x(d.month) } )
                    .attr("cy", function(d) { return y(d.height) } )
                    .attr("r", 4)
                    .attr("fill", "#69b3a2")

            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 2.5)
                .attr("d", d3.line()
                .x(function(d) { return x(d.month) })
                .y(function(d) { return y(d.height) }));
        },
        error: function(xhr){
            alert('Please enter valid date')
        }
    });
});
















//(function() {
//    const dataviz = document.getElementById('linechart');
//    $("#submit").click(function(event) {
//        $.get('/announcements', function(jd) {
//            jd.forEach(i => {
//                const div = document.createElement('div');
//                div.textContent = i.height;
//
//                dataviz.append(div);
//            });
//       });
//    });
//});

