<template>
  <v-app>
    <v-main class="d-flex justify-content-center align-center">
      <v-container fluid>
        <Nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'MainLayout',
  data: () => ({

  }),
  mounted() {
    let user = this.$store.getters["app/get_user"]

    if(this.$route.name !== "index") {
      if(user === null || user === "null") {
        alert("로그인을 먼저 해주세요.")
        this.$router.push("/")
      }
    }
  },
  methods: {

  }
}
</script>
