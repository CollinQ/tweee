import React from 'react'
import { View, SafeAreaView, Text } from 'react-native'

import { DrawerActions } from '@react-navigation/native'
import FontIcon from 'react-native-vector-icons/FontAwesome5'
import { colors } from 'theme'

const styles = {
  root: {
    flex: 1,
    flexDirection: 'column',
    paddingHorizontal: 10,
  },
  head: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },
  main: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
}

const DrawerMenu = (props) => (
  <SafeAreaView style={styles.root}>
    <View style={styles.head}>
      <FontIcon.Button
        name="times"
        size={20}
        color={colors.gray}
        backgroundColor="white"
        onPress={() => {
          props.navigation.dispatch(DrawerActions.closeDrawer())
        }}
      />
    </View>
    <View style={styles.main}>
      <Text>Drawer Menu</Text>
    </View>
  </SafeAreaView>
)

export default DrawerMenu
