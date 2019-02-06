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
                            dogs.push({species: dogSpecies, score: doggo.score, percent: 0});
                            continue;
                        }
                        maxValue = Math.max(maxValue, doggo.score);
                        dogs.push({species: dogSpecies, score: doggo.score, percent: doggo.score/maxValue*100});
                    }
                    for(let i = 0; i < Math.min(dogs.length, bars.length); i++){
                        let barString = dogs[i].species+": "+dogs[i].score
                        let originalWidth = $(bars[i]).width() / $(bars[i]).parent().width() * 100;
                        if($(bars[i]).children().text() != (barString)){
                            $(bars[i]).children().text(barString);
                            if(firstLoad && i != 0){
                                if(originalWidth < dogs[i].percent){
                                    $(bars[i]).animate({width: Math.max(0, dogs[i].percent-5)+"%"}, 500);
                                } else {
                                    $(bars[i]).animate({width: Math.min(100, dogs[i].percent+5)+"%"}, 500);
                                }
                            }
                        }
                        if(originalWidth != dogs[i].percent){
                            $(bars[i]).animate({width: dogs[i].percent+"%"}, 1000);
                        }
                    }
                    console.log("Updated bars");
                    console.log(firstLoad);
                    if(!firstLoad){
                        $('.loader-5').hide();
                        $('.bar-container').show();
                        firstLoad = true;
                    }
                }});
    }, 5000)
});