<template>
  <!-- App.vue -->
  <v-app>
    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click="drawer=!drawer"></v-app-bar-nav-icon>
      <v-toolbar-title style="cursor: pointer" @click="$router.push('/')">投票アプリ</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn text>マイページ</v-btn>
        <v-menu offset-y>
          <template v-slot:activator="{on}">
          <v-btn v-on="on" text>設定<v-icon>mdi-menu-down</v-icon></v-btn>
          </template>
          <v-list>
            <v-subheader>よく使うもの</v-subheader>
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
        <v-list dense nav>
          <v-list-item v-for="nav_list in availableMenus" :key="nav_list.name" :to="nav_list.link">
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
    link: '/vote',
    isStaff:false,
  },
  {
    name: '投票履歴を見る',
    icon: 'mdi-history',
    link: '/vote-history',
    isStaff:false,
  },
  {
    name: '投票総数を見る',
    icon: 'mdi-file-table-box-multiple-outline',
    link: '/vote-result',
    isStaff:true,
  },
  {
    name: '投票を開始する',
    icon: 'mdi-calendar-start',
    link: '/vote-start',
    isStaff:true,
  },
],
    drawer: null,
    supports:[
      {name: 'ここに',icon: 'mdi-vuetify'},
      {name: '設定を',icon: 'mdi-discord'},
      {name: '追加することが',icon: 'mdi-bug'},
      {name: 'できる',icon: 'mdi-github'},
      {name: '将来的に',icon: 'mdi-stack-overflow'},
    ],
  }),
  computed: {
    availableMenus() {
      let available = [];
      for (const menu of this.nav_lists) {
        if (!menu.isStaff) {
          available.push(menu);
        } else {
          if (this.isAvailable()) {
            available.push(menu);
          }
        }
      }
      return available;
    }
  },
  methods: {
    isAvailable() {
      return this.$store.state.isStaff
    },
  },
};
</script>