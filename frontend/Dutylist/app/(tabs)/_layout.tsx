import { Tabs } from "expo-router";

export default () => {
    return (
        <Tabs screenOptions={{ headerShown: false }}>
            <Tabs.Screen name="index"/>
            <Tabs.Screen name="products"/>
            <Tabs.Screen name="profile"/>
        </Tabs>
    );
}