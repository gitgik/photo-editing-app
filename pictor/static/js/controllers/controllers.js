'use strict';
angular.module('pictor.controllers', ['ngMaterial'])
.controller('AuthController', ['$rootScope', '$scope', '$state', '$localStorage',
    function AuthController($rootScope, $scope, $state, $localStorage) {
        $scope.login = function () {
            $localStorage.authenticated = true;
            window.location.href = "http://localhost:8000/account/facebook/login";
        };
    }])

.controller('MainController', function($scope, $rootScope, $state, $localStorage) {

})
