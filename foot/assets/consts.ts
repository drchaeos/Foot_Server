export const ROUTERS = [
  { title: '센서관리', icon: 'mdi-chart-bubble', to: '/sensor/device',
    sub: [
      { title: '센서 현황', icon: 'mdi-view-dashboard', to: "/"},
      { title: '사용자관리', icon: 'mdi-account-multiple-outline', to: "/sensor/user"},
    ]
  },
]
