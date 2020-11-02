
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


function onPageLoad() {
  console.log( "document loaded" );
  var url = '/get_movies_list'; // Use this if you are NOT using nginx 
  
  // var url = "/api/get_movies_list"; // Use this if  you are using nginx.
  $.get(url,function(data, status) {
      console.log("got response for get_movies_list request");
      if(data) {
          var movies_name_list = data.movies_list;
          $('#uimovieName_1').empty();
          for(var i in movies_name_list) {
              var opt = new Option(movies_name_list[i]);
              $('#uimovieName_1').append(opt);
          }
        
          $('#uimovieName_2').empty();
          for(var i in movies_name_list) {
              var opt = new Option(movies_name_list[i]);
              $('#uimovieName_2').append(opt);
          }
      }
  });

  var review_submit = document.getElementsByClassName('submit-1')[0]
  review_submit.addEventListener('click', onClickedPredictReview)

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

  var url = '/predict_movies';

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
  var revResult = document.getElementById("rev-result");

  var url = '/predict_review'; //Use this if you are NOT using nginx 

  // var url = "/api/predict"; // Use this if  you are using nginx.

  $.post(url, {
      review: myReview.value
  },function(data, status) {
      console.log(data.my_prediction.toString());

      var pos_review = "Great! This is the Positive review.";
      var neg_review = "Oops! This is the Negative review.";
      if(data.my_prediction == pos_review){
         revResult.innerHTML = "<span style=\"color:green\">  Great! This is the Positive review. &#128525; </span>";
      }
      else if(data.my_prediction == neg_review){
        revResult.innerHTML = "<span style=\"color:red\">  Oops! This is the Negative review. &#128532;  </span>";
      }


      console.log(status);
  });

}


window.onload = onPageLoad;