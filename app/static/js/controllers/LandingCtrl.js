app.controller('LandingCtrl', ['$scope','$http','$location', function($scope,$http,$location){
	if(localStorage.userID != null){
		$location.url("/home")
	}	
}])