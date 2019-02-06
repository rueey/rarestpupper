"use strict";

$(document).ready(function(){
    let bars = ['#bar--1', '#bar--2', '#bar--3', '#bar--4', '#bar--5']
    $('#bar--1, #bar--2, #bar--3, #bar--4, #bar--5').click(function(){
        $(this).toggleClass('expanded-bar'); //needs fixing
    });

    function parseName(dogSpecies){
        let tokens = dogSpecies.split("_");
        let ret = "";
        for(let s of tokens){
            ret += s[0].toUpperCase() + s.substring(1) + " ";
        }
        return ret.trim();
    }

    let firstLoad = false;

    setInterval(function(){
        $.ajax({url: "/api/leaderboard",
                success: function(result){
                    let dogs = [];
                    let maxValue = 0;
                    for(let doggo of result.data){
                        let dogSpecies = parseName(doggo.name);
                        if(doggo.score == 0){
                            dogs.push({species: dogSpecies, score: doggo.score, percent: "0"});
                            continue;
                        }
                        maxValue = Math.max(maxValue, doggo.score);
                        dogs.push({species: dogSpecies, score: doggo.score, percent: (doggo.score/maxValue*100).toString()});
                    }
                    for(let i = 0; i < Math.min(dogs.length, bars.length); i++){
                        $(bars[i]).css('width', dogs[i].percent+"%"); 
                        $(bars[i]).children().text(dogs[i].species+": "+dogs[i].score);
                    }
                    console.log("Updated bars");
                    if(!firstLoad){
                        $('.loader-5').hide();
                        $('.bar-container').show();
                        firstLoad = true;
                    }
                }});
    }, 5000)
});