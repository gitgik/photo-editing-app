'use strict';
angular.module('pictor.controllers', ['ngMaterial'])
.controller('AuthController', ['$rootScope', '$scope', '$state', '$localStorage', 'Restangular', 'Facebook',
    function AuthController($rootScope, $scope, $state, $localStorage, Restangular, Facebook) {
        $scope.login = function () {
            $scope.user = {};
            Facebook.login().then(function(response) {
                // get the response from a successful JS sdk login
                var obj = {
                    "accessToken": response.authResponse.accessToken,
                    "userID": response.authResponse.userID
                }
                var req = Restangular.all('api/login/');
                req.post(obj).then(function(response) {
                    $scope.user = {};
                    $localStorage.authenticated = true;
                    $localStorage.currentUser = response.extras;
                    $localStorage.currentUser.avatar = response.profile_photo;
                    console.log(JSON.stringify($localStorage.currentUser));
                    $state.go('dashboard');
                }, function(err) {
                    $scope.login = {}
                    $scope.login.err = 'Oops! Could not log in using facebook.';
                })
            })
        };
        $scope.date = {}
        $scope.date.now = new Date();
    }])

.controller('MainController', ['$rootScope', '$scope', '$state', '$localStorage', '$mdSidenav', 'Menu', 'Restangular', 'PhotoRestService',
    function($scope, $rootScope, $state, $localStorage, $mdSidenav, Menu, Restangular, PhotoRestService) {
    $scope.user = {};
    $scope.render = {};
    $scope.user.name = $localStorage.currentUser.first_name;
    $scope.user.avatar = $localStorage.currentUser.avatar;
    $scope.toggleLeft = Menu.toggle('left');
    $scope.close = function () {
        $mdSidenav('left').close()
            .then(function () {});
    }

    // populate gallery with photos
    Restangular.all('api/photos/').getList().then(function(response) {
        $scope.user.photos = response;
    });

    $scope.selectImage = function (photo_url) {
        $scope.render.selectedPhoto = photo_url
    }

    $scope.showFilters = function (photo) {
        PhotoRestService.Filters.getAll({ "image_url": photo})
        .$promise.then(function(response) {
            $rootScope.imageFilter = response;
        });
    };


}])
