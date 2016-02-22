
'use strict';

var app = angular.module('pictor',
    [
        'ui.router',
        'ngMaterial',
        'angularMoment',
        'ngResource',
        'ngStorage',
        'pictor.controllers',
    ]);

app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', '$httpProvider',
    function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {

    $stateProvider
        .state('login', {
            url: '/login',
            controller: 'AuthController',
            templateUrl: '/static/views/login.html',
            module: 'public'
        })

        .state('logout', {
            url: '/logout',
            controller: function($rootScope, $state, $localStorage) {
                $localStorage.$reset();
                $state.go('login', {}, {
                    reload: true
                });
            },
            module: 'private'
        })

    $urlRouterProvider.otherwise('/login');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
}]);

app.run(function($rootScope, $state, $localStorage) {
    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
        if (toState.module === 'private' && !$localStorage.authenticated) {
            // If logged out and transitioning to a logged in page:
            event.preventDefault();
            $state.go('login', {}, {
                reload: true
            });
        }
        if (toState.module === 'public' && $localStorage.authenticated) {
            event.preventDefault();
            $state.go('dashboard', {}, {
                reload: true
            });
        }
    });
});
