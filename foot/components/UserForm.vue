<template>
  <v-card light>
    <div class="pa-5">
      <div class="d-flex align-center">
        <span class="text-h4 font-weight-bold"> 회원 등록 </span>
        <v-spacer />
        <v-icon color="black" @click="close_modal" x-large>
          mdi-close
        </v-icon>
      </div>

      <v-form v-model="valid" ref="form" lazy-validation>
        <div class="pa-4">
          <v-text-field
              persistent-hint
              v-model="form.uid"
              color="rgba(0, 0, 0, 0.6)"
              label="회원 아이디"
              :rules="[rules.required]"
              required
          ></v-text-field>

          <v-text-field
              v-model="form.password"
              :type="is_pwd_show ? 'text' : 'password'"
              color="rgba(0, 0, 0, 0.6)"
              label="비밀번호"
              :rules="[rules.required]"
              required
              :append-icon="is_pwd_show ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append="is_pwd_show = !is_pwd_show"
          ></v-text-field>

          <v-text-field
              v-model="form.password_re"
              :type="is_pwd_show ? 'text' : 'password'"
              color="rgba(0, 0, 0, 0.6)"
              label="비밀번호 확인"
              :rules="[rules.required]"
              required
              :append-icon="is_pwd_show ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append="is_pwd_show = !is_pwd_show"
          ></v-text-field>

          <v-text-field
              v-model="form.name"
              color="rgba(0, 0, 0, 0.6)"
              label="회원 이름"
          ></v-text-field>

          <v-text-field
              v-model="form.email"
              color="rgba(0, 0, 0, 0.6)"
              label="회원 이메일"
          ></v-text-field>

          <v-text-field
              v-model="form.phone"
              color="rgba(0, 0, 0, 0.6)"
              label="회원 연락처"
          ></v-text-field>

          <v-btn block color="#222" class="font-weight-bold text-h5 text--primary" large @click="save">
            <span class="white--text"> 등록 </span>
            <v-progress-circular
                v-show="is_save"
                indeterminate
                color="white"
            ></v-progress-circular>
          </v-btn>
        </div>
      </v-form>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "SensorUserForm",
  data: () => ({
    form: {
      uid: "",
      name: "",
      email: "",
      password: "",
      password_re: "",
      phone: ""
    },
    is_save: false,
    is_edit: false,
    is_pwd_show: false,
    rules: {
      required: value => !!value || '필수사항입니다.'
    },
    valid: true
  }),
  computed: {
    user() {
      return this.$store.getters["sensor/get_selected_user"]
    },
  },
  mounted(){
    if(this.user !== null) {
      Object.assign(this.form, this.user)
      this.is_edit = true
    } else {
      this.init_form()
      this.is_edit = false
    }
  },
  watch: {
    user (value) {
      if(value !== null) {
        Object.assign(this.form, value)
        this.is_edit = true
      } else {
        this.init_form()
        this.is_edit = false
      }
    }
  },
  methods: {
    close_modal() {
      this.$store.commit("app/set_selected_user", null )
      this.$emit("close_modal")
    },
    async save() {
      if(this.form.password !== this.form.password_re) {
        alert("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return
      }

      await this.$store.dispatch("app/regist_user", this.form)

      this.init_form()
      this.close_modal()
      this.$store.dispatch("app/fetch_user_list")
    },
    init_form() {
      this.form.name = ""
      this.form.uid = ""
      this.form.password = ""
      this.form.password_re = ""
      this.form.email = ""
      this.form.phone = ""
    }
  }
}
</script>
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
nuxt_admin_airtech/SensorUserForm.vue at master · airtech306/nuxt_admin_airtech