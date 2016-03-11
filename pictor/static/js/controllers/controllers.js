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
                    "userID": response.authResponse.userID,
                    "backend": "facebook"
                }
                var req = Restangular.all('api/login/');
                req.post(obj).then(function(res) {
                    $scope.user = {};
                    $localStorage.authenticated = true;
                    $localStorage.userID = response.authResponse.userID;
                    $localStorage.currentUser = res.user;
                    console.log(JSON.stringify($localStorage.currentUser));
                    $state.go('dashboard');
                }, function(err) {
                    $scope.login = {};
                    $scope.login.err = 'Oops! Could not log in using facebook.';
                })
            })
        };
        $scope.date = {}
        $scope.date.now = new Date();
    }])

.controller('MainController', ['$rootScope', '$scope', '$state', '$localStorage', '$mdSidenav', 'Menu', 'Restangular', 'Upload','PhotoRestService',
    function($scope, $rootScope, $state, $localStorage, $mdSidenav, Menu, Restangular, Upload, PhotoRestService) {

    $scope.items = [];
    for (var i = 0; i < 1000; i++) {
        $scope.items.push(i);
    }

    $scope.user = {};
    $scope.render = {};
    $scope.user.name = $localStorage.currentUser;
    $scope.user.id = $localStorage.userID;
    $scope.toggleLeft = Menu.toggle('left');
    $scope.close = function () {
        $mdSidenav('left').close()
            .then(function () {});
    }

    // populate gallery with photos
    Restangular.all('api/photos/').getList().then(function(response) {
        $scope.user.photos = response;
        delete $localStorage.initialImage;
    });

    $scope.$on('updatePhotos', function() {
        // populate images in the gallery
        Restangular.all('api/photos/').getList().then(function(response) {
            $scope.user.photos = response;
            delete $localStorage.initialImage;
        });
    });

    $scope.$on('doneLoadingFilters', function() {
        // populate images filters in the gallery effects container
        $rootScope.doneLoadingFilters = true;
        delete $scope.render.loading;
    });

    $scope.uploadPhoto = function (file) {
        var photo = Upload.rename(file, 'PHOTO_' + Date.now().toString() +
            file.name.substr(file.name.lastIndexOf('.'), file.name.length));
        Upload.upload({
            url: 'api/photos/',
            data: {
                image: photo,
                name: photo.name
            }
        }).then(function (response) {
            $scope.$emit('updatePhotos');
            console.log('Success ' + response.config.data.image.name + 'uploaded. Response: ' + response.data);
        }, function (error) {
            console.log('Error status: ' + error.status);
        }, function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            console.log('progress: ' + progressPercentage + '% ' + evt.config.data.image.name);
        });
    };

    $scope.selectImage = function (photo_url) {
        $scope.render.selectedPhoto = photo_url
        $localStorage.initialImage = photo_url
        $scope.render.loading = true;
        delete $rootScope.doneLoadingFilters;
    };

    $scope.applyEffect = function(photo_url) {
        $scope.render.selectedPhoto = photo_url
        $scope.render.editingMode = true;
    };

    $scope.showFilters = function (photo) {
        $rootScope.effects = $rootScope.effects || {};
        PhotoRestService.Filters.getAll({ "image_url": photo})
        .$promise.then(function(response) {
            $rootScope.effects.url = response;
            $scope.$emit('doneLoadingFilters');
        });
        $scope.render.editingMode = false;
    };

    $scope.clearCanvas = function () {
        $scope.render.selectedPhoto = undefined;
        $scope.render.editingMode = false;
        delete $localStorage.initialImage;
    }

    $scope.restoreOrigin = function(image) {
        $scope.render.selectedPhoto = $localStorage.initialImage;
        $scope.render.editingMode = false;
    }
}])
