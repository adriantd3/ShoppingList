
import {Animated} from 'react-native';

export const onPressInCard = (scaleValue) => {
    Animated.timing(scaleValue, {
        toValue: 0.95,
        duration: 150, // Duración en milisegundos
        useNativeDriver: true,
    }).start();
}

export const onPressOutCard = (scaleValue) => {
    Animated.timing(scaleValue, {
        toValue: 1,
        duration: 150, // Duración en milisegundos
        useNativeDriver: true,
    }).start();
}