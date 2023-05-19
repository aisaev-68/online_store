var mix = {
    methods: {
        setTag (id) {
            this.topTags = this.topTags.map(tag => {
                return  tag.id === id
                    ? {
                        ...tag,
                        selected: !tag.selected
                    }
                    : tag
            })
            this.getCatalogs()
        },
        setSort (id) {
            if (this.selectedSort?.id === id) {
                this.selectedSort.selected =
                    this.selectedSort.selected === 'dec'
                        ? 'inc'
                        : 'dec'
            } else {
                if (this.selectedSort) {
                    this.selectedSort = null
                }
                this.selectedSort = this.sortRules.find(sort => sort.id === id)
                this.selectedSort = {
                    ...this.selectedSort,
                    selected: 'dec'
                }
            }
            this.getCatalogs()
        },
        getTags() {
            this.getData('/api/tags', { category: this.category })
                .then(data => this.topTags = data.map(tag => ({
                    ...tag,
                    selected: false
                })))
                .catch(() => {
                        this.topTags = []
                        console.warn('Ошибка получения тегов')
                })

        },
        getCatalogs(page) {
            if(typeof page === "undefined") {
                page = 1
            }
            const PAGE_LIMIT = 6
            const tags = this.topTags.filter(tag => !!tag.selected).map(tag => tag.id)
            this.getData("/api/catalog", {
                page,
                category: this.category,
                sort: this.selectedSort ? this.selectedSort.id : null,
                sortType: this.selectedSort ? this.selectedSort.selected : null,
                filter: this.filter,
                tags,
                limit: PAGE_LIMIT
            })
                .then(data => {
                    this.catalogCards = data.items
                    this.currentPage = data.currentPage
                    this.lastPage = data.lastPage

                }).catch(() => {
                    console.warn('Ошибка при получении каталога')
                })
        }
    },
    mounted() {
        this.selectedSort = this.sortRules?.[1]
            ? { ...this.sortRules?.[1], selected: 'inc' }
            :  null

        this.getCatalogs()
        this.getTags()
//        window.alert("THIS.TAGS ", getTags())
//        this.category = location.pathname.startsWith('/catalog/')
//            ? Number(location.pathname.replace('/catalog/', ''))
//            : null
    },
     created: function(){
            this.category = window.location.pathname.startsWith('/api/catalog/')
                ? Number(window.location.pathname.split('/')[3])
                : null
//            window.alert(this.category)
      },

    data() {
        return {
            pages: 1,
            category: null,
            catalogCards: [],
            currentPage: null,
            lastPage: 1,
            selectedSort: null,
            filter: {
                name: '',
                minPrice: 0,
                maxPrice: 50000,
                freeDelivery: false,
                available: true
            }
        }
    }
}