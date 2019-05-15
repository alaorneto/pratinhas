var extrato = new Vue({
    delimiters: ['[[', ']]'],
    el: '#extrato',
    data: {
        dados: false,
        extrato: null,
    },
    methods: {
        atualiza_extrato: function () {
            this.dados = !this.dados;
        },
    },
    mounted() {
        this.atualiza_extrato();
    },
});