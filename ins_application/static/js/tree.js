var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    g = svg.append("g").attr("transform", "translate(40,0)");

var tree = d3.cluster()
    .size([height, width - 160]);

var stratify = d3.stratify()
    .parentId(function(d) { return d.id.substring(0, d.id.lastIndexOf(".")); });

d3.csv("/flare.csv", function(error, data) {
  if (error) throw error;

  var root = stratify(data)
      .sort(function(a, b) { return (a.height - b.height) || a.id.localeCompare(b.id); });

  tree(root);

  var link = g.selectAll(".link")
      .data(root.descendants().slice(1))
    .enter().append("path")
      .attr("class", "link")
      .attr("d", function(d) {
        return "M" + d.y + "," + d.x
            + "C" + (d.parent.y + 100) + "," + d.x
            + " " + (d.parent.y + 100) + "," + d.parent.x
            + " " + d.parent.y + "," + d.parent.x;
      });

  var node = g.selectAll(".node")
      .data(root.descendants())
    .enter().append("g")
      .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

  node.append("circle")
      .attr("r", 2.5);

  var text = node.append("text")
      .attr("dy", 3)
      .attr("x", function(d) { return d.children ? 20 : 2; })
      .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
      //.attr("textstr", function(d) { return d.id.substring(d.id.lastIndexOf(".") + 1)});
      .text(function(d) { 
        var name = d.id.substring(d.id.lastIndexOf(".") + 1);
        if (name.length > 6){
          return name.substring(0, 6) + "..";
        }else{
          return name;
        }
      })
      .append("svg:title")
      .text(function(d) {
        var name = d.id.substring(d.id.lastIndexOf(".") + 1);
        return name;
      });
      /*
      .on("mouseover", function(d){
          var name = d.id.substring(d.id.lastIndexOf(".") + 1);
          console.log(name);
      });
      */
  /*
  node.selectAll("text").selectAll(function(d){
     var arr_ = split_text(d.id.substring(d.id.lastIndexOf(".") + 1));
     console.log(d);
     .selectAll("tspan")
     .enter()
     .append("tspan")
     .attr("x", d.attr("x"))  
     .attr("dy", "1em")  
     .text(function(d){return d.attr("textstr")});
  });
  */
});

function split_text(str_){
  //console.log(str_);
  var strArr = [];
  var n = 6;
  for (var i = 0, l = str_.length; i < l/n; i++) {
    var a = str_.slice(n*i, n*(i+1));
    strArr.push(a);
  }
  return strArr;
}