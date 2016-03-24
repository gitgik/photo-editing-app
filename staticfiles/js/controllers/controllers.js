'use strict';
angular.module('picto.controllers', ['ngMaterial'])
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

.controller('MainController', ['$rootScope', '$scope', '$state', '$location', '$localStorage', '$mdSidenav', '$mdDialog', 'Menu', 'Restangular', 'Upload','PhotoRestService', 'Toast',
    function($scope, $rootScope, $state, $location, $localStorage, $mdSidenav, $mdDialog, Menu, Restangular, Upload, PhotoRestService, Toast) {

    $scope.user = {};
    $scope.render = {};
    $localStorage.filters = {};
    $scope.user.name = $localStorage.currentUser;
    $scope.user.id = $localStorage.userID;
    $scope.toggleLeft = Menu.toggle('left');
    $scope.close = function () {
        $mdSidenav('left').close()
            .then(function () {});
    }

    // url for sharing
    var url = $location.host(),
        port = $location.port(),
        protocol = $location.protocol();

    url = protocol + '://' + url + ':' + port + '/';

    // populate gallery with photos
    Restangular.all('api/photos/').getList().then(function(response) {
        if (response.length == 0) {
            $scope.$emit('noPhotos');
            $scope.user.noPhotos = true;
        }
        else {
            $scope.user.noPhotos = false;
            $scope.user.photos = response;
            delete $localStorage.initialImage;
        }
    });

    $scope.$on('noPhotos', function() {
        $scope.user.noPhotos = true;
        delete $scope.user.photos;
    });

    $scope.$on('updatePhotos', function() {
        // populate images in the gallery
        Restangular.all('api/photos/').getList().then(function(response) {
            if (response.length == 0) {
                $scope.$emit('noPhotos');
            }
            else {
                delete $scope.user.noPhotos;
                $scope.user.photos = response;
            }
            delete $localStorage.initialImage;
        });
    });

    $scope.$on('doneLoadingFilters', function() {
        // populate images filters in the gallery effects container
        $rootScope.doneLoadingFilters = true;
        delete $scope.render.loading;
        $rootScope.effects.init =false;
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
            Toast.show('Photo uploaded.');
        }, function (error) {
            console.log('Error status: ' + error.status);
            Toast.show('Photo not uploaded. Please try again');
        }, function (evt) {
            $scope.render.progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            if ($scope.render.progressPercentage == 100) {
                delete $scope.render.progressPercentage;
            }
        });
    };

    $scope.savePhoto = function(photo, photoID) {
        var data = {
            effect: photo,
            photo_id: photoID
        }
        PhotoRestService.ImageEffects.save(
            data, function(res) {
                Toast.show('Photo saved');
                $scope.$emit('updatePhotos');
            }, function(error) {
                Toast.show('Could not save photo. Check your internet connectivity.')
            });
    };

    $scope.selectImage = function (photo) {
        delete $rootScope.doneLoadingFilters;
        $scope.render.selectedPhoto = photo.image;
        $rootScope.selectedPhotoID = photo.id;
        $localStorage.initialImage = photo.image;
        $scope.render.loading = true;
    };

    $scope.applyEffect = function(photo_url) {
        $scope.render.selectedPhoto = photo_url
        $scope.render.editingMode = true;
    };

    $scope.showFilters = function (photo) {
        $rootScope.effects = $rootScope.effects || {};
        $rootScope.effects.init = true;
        var photoID = photo.id;

        if ($localStorage.filters[photoID] !== undefined) {
            $rootScope.effects.url = $localStorage.filters[photoID];
            $scope.$emit('doneLoadingFilters');
        }
        else {
            var image = photo.image;
            PhotoRestService.Filters.getAll({ "image_url": image })
            .$promise.then(function(response) {
                $rootScope.effects.url = response;
                $localStorage.filters[photoID] = $rootScope.effects.url;
                $scope.$emit('doneLoadingFilters');
            });
        }
        $scope.render.editingMode = false;
    };

    $scope.clearCanvas = function () {
        $scope.render.selectedPhoto = undefined;
        $rootScope.selectedPhotoID = undefined;
        $scope.render.editingMode = false;
        delete $localStorage.initialImage;
    };

    $scope.restoreOrigin = function(image) {
        $scope.render.selectedPhoto = $localStorage.initialImage;
        $scope.render.editingMode = false;
    };

    // Share a photo
    $scope.sharePhoto = function (photo) {
        if (photo !== undefined) {
            FB.ui({
                method: 'feed',
                link: photo,
                caption: "",
                picture: photo,
                message: ''
            }, function(response) {
                if (response.error_code != 4201) {
                    console.log(response)
                    Toast.show('Photo shared on Facebook');
                }
            }, function(error) {
                Toast.show('Your photo could not be shared. Please try again')
            });
        }
    };

    $scope.photoDelConfirm = function(ev, photoID) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
          .title('Are you sure?')
          .textContent('delete this photo?')
          .ariaLabel('delete')
          .targetEvent(ev)
          .ok('DELETE')
          .cancel('CANCEL');
        $mdDialog.show(confirm).then(function() {
            PhotoRestService.ModifyImage.deleteImage(
            {id: photoID}, function (response) {
                if ($rootScope.selectedPhotoID == photoID) {
                    delete $scope.render.selectedPhoto;
                }
                $scope.$emit('updatePhotos');
                delete $localStorage.filters[photoID];
                Toast.show('Photo deleted');
            }, function(error) {
                console.log('ERROR: ' + error)
            });
        }, function() {});
    };


    $scope.photoDelInEditMode = function(ev, photoID) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
              .title('Are you sure?')
              .textContent('delete this photo with all it\'s filters?')
              .ariaLabel('delete')
              .targetEvent(ev)
              .ok('DELETE')
              .cancel('CANCEL');
        $mdDialog.show(confirm).then(function() {
            PhotoRestService.ModifyImage.deleteImage(
            {id: photoID}, function (response) {
                $scope.$emit('updatePhotos');
                delete $scope.render.selectedPhoto;
                delete $localStorage.filters[photoID];
                Toast.show('Photo deleted');
            });
        }, function() {});
    };
}])
