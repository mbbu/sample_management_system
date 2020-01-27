import Vue from 'vue';

export const EventBus = new Vue()

export function isValidJwt (jwt) {
    if(!jwt || jwt.split('.').length < 3) {
    return false
    }
    const data = JSON.parse(atob(jwt.split('.') [1]))
    const exp = new Data(date.exp * 1000) // dates in milliseconds
    const now = new Date()
    return now < exp
}
