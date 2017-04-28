app.controller('RegisterCtrl', ['$scope','$location','$http', function($scope,$location,$http){
	if(localStorage.userID != null){
		$location.url("/home")
	}

	$scope.register = function(){
		url = "/api/register"

		config = {
			headers:{
				"Content-Type":"application/json"
			}
		}

		data={
			"fname":$scope.fname,
			"lname":$scope.lname,
			"id":$scope.studentID,
			"password":$scope.password
		}

		$http.post(url, data, config).then(function(response){
			console.log(response.data)
			if(response.data.status =="success"){
				$location.url('/')
			}else{
				console.log(response.data.message)
			}
		})
	}
	
}])