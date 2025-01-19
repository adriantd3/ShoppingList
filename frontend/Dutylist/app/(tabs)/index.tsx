import { Link } from 'expo-router';
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Button, ButtonText } from '@/components/ui/button';

const HomePage = () => {
    return (
        <View style={styles.container}>
            <Link href="/auth">Go to Login</Link>
            <Text style={styles.text}>Hello, I am home</Text>
            <Button>
                <ButtonText>Click me</ButtonText>
            </Button>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#fff',
    },
    text: {
        fontSize: 20,
        fontWeight: 'bold',
    },
});

export default HomePage;