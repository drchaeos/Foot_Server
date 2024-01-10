<template>
  <v-row>

    <v-col style="font-size: 40px; text-align: center; font-weight: bold">
      <div style="padding-bottom: 120px"> AI Foot Diagnosis </div>

      <v-row style="width: 50%; margin: auto">
        <v-col>
          <v-row>
            <v-col>
              <v-text-field
                  v-model="form.id"
                  class="rounded-b-0"
                  type="id"
                  placeholder="아이디"
                  color="secondary"
                  hide-details
                  outlined
                  @keyup.enter="login"
                  prepend-inner-icon="mdi-account-circle-outline"
                  autofocus
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                  placeholder="패스워드"
                  color="secondary"
                  v-model="form.password"
                  class="rounded-t-0"
                  type="password"
                  hide-details
                  outlined
                  @keyup.enter="login"
                  prepend-inner-icon="mdi-lock"
                  autocomplete="off"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row style="width: 50%; margin: auto">
        <v-col>
          <v-btn class="mt-6 pa-5 secondary white--text rounded-0" block @click="login">로그인</v-btn>
        </v-col>
      </v-row>
    </v-col>

  </v-row>
</template>

<script>
export default {
  name: 'IndexPage',
  layout: "MainLayout",
  data: ()  =>  ({
    form: {
      id: "",
      password: "",
    },
  }),
  methods: {
    login() {
      this.$store.dispatch("app/login", this.form)
      .then(res => {
        let user = this.$store.getters["app/get_user"]

        if(user["id"] !== undefined) {
          this.$router.push("main")
        }
      })
    }
  }
}
</script>
