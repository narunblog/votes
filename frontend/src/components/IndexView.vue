<template>
  <!-- App.vue -->
  <v-app>
    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click="drawer=!drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Vuetify</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn text>For Enterprise</v-btn>
        <v-menu offset-y>
          <template v-slot:activator="{on}">
          <v-btn v-on="on" text>Support<v-icon>mdi-menu-down</v-icon></v-btn>
          </template>
          <v-list>
            <v-subheader>Get help</v-subheader>
            <v-list-item v-for="support in supports" :key="support.name">
            <v-list-item-icon>
              <v-icon>{{ support.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ support.name }}</v-list-item-title>
            </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar-items>
    </v-app-bar>

    <v-navigation-drawer app v-model="drawer" clipped>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title grey--text text--darken-2">
              Navigation lists
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list dense nav>
          <v-list-item v-for="nav_list in nav_lists" :key="nav_list.name" :to="nav_list.link">
            <v-list-item-icon>
              <v-icon>{{ nav_list.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ nav_list.name }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
    </v-navigation-drawer>

    <!-- アプリケーションのコンポーネントに基づいてコンテンツのサイズを決定 -->
    <v-main>

      <!-- アプリケーションに適切なgutterを提供 -->
      <v-container fluid>
        <!-- vue-routerを使用する場合 -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    nav_lists:[
  {
    name: '投票',
    icon: 'mdi-vote',
    link: '/vote-select',
  },
  {
    name: '投票履歴を見る',
    icon: 'mdi-history',
    link: '/vote-history',
  },
  {
    name: '投票総数を見る',
    icon: 'mdi-file-table-box-multiple-outline',
    link: '/vote-result',
  },
  {
    name: '投票を開始する',
    icon: 'mdi-calendar-start',
    link: '/vote-start',
  },
],
    drawer: null,
    supports:[
      {name: 'Consulting and suppourt',icon: 'mdi-vuetify'},
      {name: 'Discord community',icon: 'mdi-discord'},
      {name: 'Report a bug',icon: 'mdi-bug'},
      {name: 'Github issue board',icon: 'mdi-github'},
      {name: 'Stack overview',icon: 'mdi-stack-overflow'},
    ],
  }),
};
</script>