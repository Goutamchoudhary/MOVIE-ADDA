
function getRating_movie1() {
  var uiRatings_1 = document.getElementsByName("uiRatings_1");
  for(var i in uiRatings_1) {
    if(uiRatings_1[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1; // Invalid Value
}


function getRating_movie2() {
  var uiRatings_2 = document.getElementsByName("uiRatings_2");
  for(var i in uiRatings_2) {
    if(uiRatings_2[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1; // Invalid Value
}


function onClickedRecommendations() {
  console.log("Recommendations button clicked")
  var result_desc = document.getElementById("result-desc");
  var result_1 = document.getElementById("result-1");
  var result_2 = document.getElementById("result-2");
  var result_3 = document.getElementById("result-3");
  var result_4 = document.getElementById("result-4");
  var result_5 = document.getElementById("result-5");
  
  var movieName1 = document.getElementById("uimovieName_1");
  var rating1 = getRating_movie1();
  var movieName2 = document.getElementById("uimovieName_2");
  var rating2 = getRating_movie2();

  var url = "http://127.0.0.1:5000/predict_movies";

  $.post(url, {
      movie_name_1: movieName1.value,
      movie_name_2: movieName2.value,
      rating_1: rating1,
      rating_2: rating2
  },function(data, status){
      console.log(data.movie1.toString());
      result_desc.innerHTML = "<p>Top 5 Recommended movies for you: </p>";
      result_1.innerHTML = "<p>1. " + data.movie1.toString() + "</p>";
      result_2.innerHTML = "<p>2. " + data.movie2.toString() + "</p>";
      result_3.innerHTML = "<p>3. " + data.movie3.toString() + "</p>";
      result_4.innerHTML = "<p>4. " + data.movie4.toString() + "</p>";
      result_5.innerHTML = "<p>5. " + data.movie5.toString() + "</p>";

      console.log(status); 
  });

}


function onClickedPredictReview() {
  console.log("Estimate review button clicked");
  var myReview = document.getElementById("uiMessage");
  var revResult = document.getElementById("ReviewStatus");

  var url = "http://127.0.0.1:5000/predict_review"; //Use this if you are NOT using nginx 

  // var url = "/api/predict"; // Use this if  you are using nginx.

  $.post(url, {
      review: myReview.toString()
  },function(data, status) {
      console.log(data.my_prediction.toString());
      revResult.innerHTML = "<h2>Prediction:  <span>  " + data.my_prediction.toString() +    "</span></h2>";

      console.log(status);
  });

}

function onPageLoad() {
  console.log( "document loaded" );
  var url = "http://127.0.0.1:5000/get_movies_list"; // Use this if you are NOT using nginx 
  
  // var url = "/api/get_movies_list"; // Use this if  you are using nginx.
  $.get(url,function(data, status) {
      console.log("got response for get_movies_list request");
      if(data) {
          var movies_name_list = data.movies_list;
          var uimovieName = document.getElementById("uimovieName_1");
          $('#uimovieName_1').empty();
          for(var i in movies_name_list) {
              var opt = new Option(movies_name_list[i]);
              $('#uimovieName_1').append(opt);
          }

          var uimovieName = document.getElementById("uimovieName_2");
          $('#uimovieName_2').empty();
          for(var i in movies_name_list) {
              var opt = new Option(movies_name_list[i]);
              $('#uimovieName_2').append(opt);
          }
      }
  });
}

window.onload = onPageLoad;