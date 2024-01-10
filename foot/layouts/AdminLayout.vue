<template>
  <v-app>
    <v-app-bar clipped-left app>
      <v-toolbar-title v-text="title" class="cursor_pointer" @click="$router.push('/')"/>
      <v-spacer/>
      <v-divider vertical />
      <span @click="logout" tile color="grey darken-3" class="cursor_pointer d-block mx-sm-4 mx-1">
        로그아웃
      </span>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <transition>
          <Nuxt />
        </transition>
        
      </v-container>
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import { ROUTERS } from "assets/consts";

export default {
  name: 'MainLayout',
  data: () => ({
    title: '관리자페이지',
    routers: ROUTERS,
  }),
  computed: {

  },
  mounted() {
    let user = this.$store.getters["app/get_user"]

    if(this.$route.name !== "index") {
      if(user === null || user === "null") {
        alert("로그인을 먼저 해주세요.")
        this.$router.push("/admin")
      }
    }
  },
  methods: {
    logout() {
      this.$store.commit("app/set_user", null)

      this.$router.push("/admin")
    }
  }
}
</script>
