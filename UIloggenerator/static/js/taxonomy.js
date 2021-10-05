/*
 * name: category
 * img: url
 * children: [{subcategories}]
 */

function taxonomytree(data) {

    /* Inital Variables */
    // Size of the svg
    var size = 800;

    var radius = 40;
    var fontSize = 20;
    var id = 0;
    var animationDuration = 750;
    var root;
    var nodeCount;

    var tree = d3.layout.tree()
        .size([size, size]);

    var diagonal = d3.svg.diagonal()
        .projection(function (d) {
            return [d.x, d.y];
        });

    var svg = d3.select("#d3Hierarchy").append("svg")
        .attr("width", size)
        .attr("height", size)
        .append("g");

    // Create a circle for cropping
    svg.append("clipPath")
        .attr("id", "circle")
        .append("circle")
        .attr("r", radius);

    // Set the root of the tree
    root = data;
    root.fromX = size / 2;
    root.fromY = 0;

    function collapse(d) {
        if (d.children) {
            d.hidden = d.children;
            d.hidden.forEach(collapse);
            d.children = null;
        }
    }

    // Collapse the inital tree down to just the root
    root.hidden = root.children;
    root.children.forEach(collapse);
    update(root);

    d3.select(self.frameElement).style("height", "800px");

    // Count the number of nodes on each line to center the tree
    function countNodes(node) {
        if (!nodeCount[node.depth]) {
            nodeCount.push(0);
        }
        nodeCount[node.depth]++;
        if (node.children) {
            node.children.forEach(countNodes);
        }
    }

    function update(source) {

        var nodes = tree.nodes(root).reverse();
        var links = tree.links(nodes);

        nodeCount = [];
        countNodes(root);

        // Set the hights of the nodes (ultimately trying to center them)
        nodes.forEach(function (d) {
            d.y = ((d.depth + 1) * size) / (nodeCount.length + 2);
        });

        /* Node Logic */
        var node = svg.selectAll("g.node")
            .data(nodes, function (d) {
                return d.id || (d.id = ++id);
            });

        // Initialize the node on entry
        var nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("transform", function (d) {
                return "translate(" + source.fromX + "," + source.fromY + ")";
            })
            

        // Set the node's image
        nodeEnter.append("image")
            .attr("xlink:href", function (d) {
                return d.img
            })
            .attr("r", 1e-6)
            .attr("clip-path", "url(#circle)")
            .on("click", click);

        // Set the node's text
        nodeEnter.append("a")
            .attr("xlink:href", function (d) {
                return d.pk;
            }).append("text")
            .attr("y", function (d) {
                return -(radius + fontSize)
            })
            .attr("data-toggle", "tooltip")
            .attr("title", function (d) {
                return d.description;
            })
            .attr("text-anchor", 'middle')
            .text(function (d) {
                return d.name;
            })
            .attr("xlink:href", function (d) {
                return d.pk;
            })
            .style("fill-opacity", 1e-6)
            .style("font-size", fontSize + "px");

        // Update the node after entry
        var nodeUpdate = node.transition()
            .duration(animationDuration)
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

        // Move the node 
        nodeUpdate.select('image')
            .attr('x', radius * -1)
            .attr('y', radius * -1)
            .attr('width', radius * 2)
            .attr('height', radius * 2)
            .style('opacity', 1)
            .each('interrupt', fixOpacity)
            .each('end', fixOpacity);

        // In case of interrupted animation, the opacity will still be one
        function fixOpacity() {
            d3.selectAll('g').style("opacity", 1);
        }

        nodeUpdate.select("text")
            .style("fill-opacity", 1);

        // Initalize the node leaving 
        var nodeExit = node.exit().transition()
            .duration(animationDuration)
            .attr("transform", function (d) {
                return "translate(" + source.x + "," + source.y + ")";
            })
            .style("opacity", 0)
            .remove();

        nodeExit.select("text")
            .style("fill-opacity", 1e-6);

        /* Link Logic */
        var link = svg.selectAll("path.link")
            .data(links, function (d) {
                return d.target.id;
            });

        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function (d) {
                var change = {
                    x: source.fromX,
                    y: source.fromY
                };
                return diagonal({
                    source: change,
                    target: change
                });
            });

        link.transition()
            .duration(animationDuration)
            .attr("d", diagonal);

        link.exit().transition()
            .duration(animationDuration)
            .attr("d", function (d) {
                var change = {
                    x: source.x,
                    y: source.y
                };
                return diagonal({
                    source: change,
                    target: change
                });
            })
            .remove();

        nodes.forEach(function (d) {
            d.fromX = d.x;
            d.fromY = d.y;
        });
    }

    // When a node is clicked, hide all of the unrelated nodes and show all the children
    function click(d) {
        if (d.parent) {
            d.parent.children = [d];
        }
        if (d.hidden) {
            d.children = d.hidden;
            d.children.forEach(hide);
        }
        update(d);
        $('[data-toggle="tooltip"]').tooltip();
    }

    function hide(d) {
        if (d.children) {
            d.hidden.forEach(hide);
            d.children = null;
        }
    }
}