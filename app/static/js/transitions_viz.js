// Adappted from: http://bl.ocks.org/rkirsling/5001347

function draw_transitions(graph){

var color = d3.scale.category20();

var width = 700,
    height = 520;

var force = d3.layout.force()
    .nodes(graph.nodes)
    .links(graph.links)
    .size([width, height])
    .linkDistance(30)
    .charge(-50)
    .on("tick", tick)
    .start();

var svg = d3.select("#transition").append("svg")
    .attr("width", width)
    .attr("height", height);

// build the arrow.
svg.append("svg:defs").selectAll("marker")
    .data(["end"])      // Different link/path types can be defined here
    .enter().append("svg:marker")    // This section adds in the arrows
    .attr("id", String)
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", -1.5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5");

// add the links and the arrows
var path = svg.append("svg:g").selectAll("path")
    .data(graph.links)
    .enter().append("svg:path")
//  .attr("class", function(d) { return "link " + d.type; })
    .attr("class", "link")
    .attr("marker-end", "url(#end)");

// define the nodes
var node = svg.selectAll(".node")
    .data(force.nodes())
    .enter().append("g")
    .attr("class", "node")
    .call(force.drag);

// add the nodes
node.append("circle")
    .attr("r", function(d){return 5 + d.deg})
    .style("fill", function(d) { return color(d.group); })
    .on("click", function(d,i) {
        //alert(d.name)
        $("#jobs").empty();
        for (var i=0; i<graph.nodes.length; i++) {
            if (graph.nodes[i].group == d.group) {
                $("#jobs").append("<button type='button' class='list-group-item'>"+graph.nodes[i].name+"</button>");
            }
        }
    })

node.append("title")
      .text(function(d) { return d.name; });

// add the text 
node.append("text")
    .attr("x", 12)
    .attr("dy", ".35em")
    .text(function(d) { if (d.deg > 1) return d.name; });

// add the curvy lines
function tick() {
    path.attr("d", function(d) {
        var dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = Math.sqrt(dx * dx + dy * dy);
        return "M" +
            d.source.x + "," +
            d.source.y + "A" +
            dr + "," + dr + " 0 0,1 " +
            d.target.x + "," +
            d.target.y;
    });

    node
        .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")"; });
}


}

