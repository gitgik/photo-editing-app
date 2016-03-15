
'use strict';

var app = angular.module('pictor',
    [
        'ui.router',
        'ngMaterial',
        'angularMoment',
        'ngResource',
        'ngStorage',
        'restangular',
        'ngFileUpload',
        'pictor.controllers',
    ]);

app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', '$httpProvider', '$mdThemingProvider',
    function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider, $mdThemingProvider) {

    $mdThemingProvider.definePalette('pictorTheme', {
        '50': '01579b', '100': '01579b', '200': '01579b',
        '300': '01579b', '400': '01579b', '500': '01579b',
        '600': '01579b', '700': '01579b', '800': '01579b',
        '900': '01579b', 'A100': '01579b', 'A200': '01579b',
        'A400': '01579b', 'A700': '01579b',
        'contrastDefaultColor': 'light',
        'contrastDarkColors': ['50', '100', // hues for dark color
         '200', '300', '400', 'A100'],
        'contrastLightColors': undefined
    });
    $mdThemingProvider.theme('default').primaryPalette('pictorTheme');

    $stateProvider
        .state('login', {
            url: '/',
            controller: 'AuthController',
            templateUrl: '/static/views/login.html',
            module: 'public'
        })

        .state('dashboard', {
            url: '/dashboard',
            controller: 'MainController',
            templateUrl: '/static/views/dashboard.html',
            module: 'private'
        })

        .state('logout', {
            url: '/logout',
            controller: function($state, $localStorage, Restangular) {
                Restangular.one('api/logout/').get().then(
                    function (response) {
                        $localStorage.$reset();
                        $state.go('login');
                    });
            },
            module: 'private'
        })

    // $urlRouterProvider.otherwise('/');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
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
