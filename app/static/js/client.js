function init() {
    $( document ).ajaxStart(function() {
        $( "#loading" ).show();
    });

    $( document ).ajaxComplete(function() {
        $( "#loading" ).hide();
    });
 
    $('#occupation_search').autocomplete({
        source: function(term, response) {
            $.getJSON( "api/auto_occupation/"+$('#occupation_search').val(), function(data) {
                response(data)
            });
        }
    })
   
    $("#occupation_go").click(function() {
         $.getJSON( "/api/occupation_skills/"+$('#occupation_search').val()+"/"+$('#occupation_skills_top').val(), function(data) {
             occupation_skills_hc(data)
         });
    })

    $("#loads_go").click(function() {
         //$.getJSON( "api/census_tract/12345/5"), function(data) {
         //    census_tract_hc(data);
         //});
    })


    $("#resume").click(function() {
         $.getJSON( "match/"+$('#resume').val(), function(data) {
             $("#onet_occupation").empty()
             $("#onet_occupation").append(data["onet"])
         });
    })


}

function occupation_skills_hc(data) {
    $("#occupation_skills_hc").highcharts(data);
}

function census_tract_hc(data) {
    $("#census_tract_current_hc").highcharts(data["loads"][0]);
    $("#census_tract_current_hc").show();
    $("#census_tract_growth_hc").highcharts(data["loads"][1]);
    $("#census_tract_growth_hc").show();
}

function init_census_map_kmeans(data){
    LeafletLib.initialize($("#census_map")[0], chicago_CBSA_tracts, [41.882726, -87.629], 12, data);
}

function draw_industry_nowcasting(data){
    $("#industry_nowcasting_hc").highcharts(data);
}

function get_nowcasting_industries_and_tracts() {
    $.getJSON( "/api/industries_and_tracts", function(data) {
        tracts = data["tracts"]
        for (var i=0; i<tracts.length; i++) {
            $("#tracts").append('<option value="'+tracts[i]+'">'+tracts[i]+'</option>');
        }
        indNames = data["indNames"]
        indCodes = data["indCodes"]
        for (var i = 0; i<indNames.length; i++) {
            $("#inds").append('<option value="'+indCodes[i]+'">'+indNames[i]+'</option>');
        }
    });
}
