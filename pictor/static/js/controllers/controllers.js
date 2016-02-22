'use strict';
angular.module('pictor.controllers', ['ngMaterial'])
.controller('AuthController', ['$rootScope', '$scope', '$state', '$localStorage',
    function AuthController($rootScope, $scope, $state, $localStorage) {
        $scope.login = function () {
            $localStorage.authenticated = true;
            $state.go('dashboard');
        };
    }])
