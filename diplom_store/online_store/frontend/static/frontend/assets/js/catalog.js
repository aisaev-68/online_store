var mix = {
  methods: {
    setTag(id) {
      this.topTags = this.topTags.map((tag) => {
        if (tag.id === id) {
          tag.selected = !tag.selected;
        } else {
          tag.selected = false;
        }
        return tag;
      });
      this.getCatalogs();
    },
    setSort(id) {
      if (this.selectedSort?.id === id) {
        this.selectedSort.selected =
          this.selectedSort.selected === 'dec' ? 'inc' : 'dec';
      } else {
        if (this.selectedSort) {
          this.selectedSort = null;
        }
        this.selectedSort = this.sortRules.find((sort) => sort.id === id);
        this.selectedSort = {
          ...this.selectedSort,
          selected: 'dec',
        };
      }
      this.getCatalogs();
    },

    getSellers() {
        this.getData('/api/sellers/')
          .then((data) => {
            this.sellers = data;
          })
          .catch(() => {
            this.sellers = [];
            console.warn('Ошибка получения продавцов');
          });
      },
      getSpecifications() {
        this.getData('/api/specifications/')
          .then((data) => {
            this.specifications = data;
          })
          .catch(() => {
            this.specifications = [];
            console.warn('Ошибка получения продавцов');
          });
      },
      getManufacturers() {
        this.getData('/api/manufacturers/')
          .then((data) => {
            this.manufacturers = data;
          })
          .catch(() => {
            this.manufacturers = [];
            console.warn('Ошибка получения производителей');
          });
      },
      updateManufacturers() {
        this.filter.manufacturers = this.manufacturers.filter((manufacturer) =>
          this.selectedManufacturers.includes(manufacturer.id)
        );
        this.getCatalogs();
      },
      updateSellers() {
        this.filter.sellers = this.sellers.filter((seller) =>
          this.selectedSellers.includes(seller.id)
        );
        this.getCatalogs();
      },
    getTags() {
      this.getData('/api/tags', { category: this.category })
        .then((data) => (this.topTags = data.map((tag) => ({ ...tag, selected: false }))))
        .catch(() => {
          this.topTags = [];
          console.warn('Ошибка получения тегов');
        });
    },
    getCatalogs(page) {
      if (typeof page === 'undefined') {
        page = 1;
      }
      const PAGE_LIMIT = 6;
      const tags = this.topTags
        .filter((tag) => tag.selected)
        .map((tag) => tag.id);

      this.category = location.pathname.startsWith('/catalog/')
        ? Number(location.pathname.replace('/catalog/', ''))
        : null;

      this.getData('/api/catalog/', {
        page,
        category: this.category,
        sort: this.selectedSort ? this.selectedSort.id : null,
        sortType: this.selectedSort ? this.selectedSort.selected : null,
        filter: {
          name: this.filter.name,
          minPrice: this.filter.minPrice,
          maxPrice: this.filter.maxPrice,
          freeDelivery: this.filter.freeDelivery,
          available: this.filter.available,
          sellers: this.filter.sellers,
          manufacturers: this.filter.manufacturers,
          specifications: this.filter.specifications,
        },
        tags,
        limit: PAGE_LIMIT,
      })
        .then((data) => {
          this.catalogCards = data.items;
          this.currentPage = data.currentPage;
          this.lastPage = data.lastPage;
        })
        .catch(() => {
          console.warn('Ошибка при получении каталога');
        });
    },
  },
  mounted() {
    this.selectedSort = this.sortRules.find((sort) => sort.id === 'price');
    this.selectedSort.selected = 'inc';

    this.getTags();
    this.getSellers();
    this.getManufacturers();
    this.updateSellers();
    this.updateManufacturers();
    this.getSpecifications();
    //this.selectedSellers = []; // список выбранных продавцов
    //this.selectedManufacturers = []; // список выбранных производителей

    this.category = location.pathname.startsWith('/catalog/')
      ? Number(location.pathname.replace('/catalog/', ''))
      : null;
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
        available: true,
        sellers: [], // список выбранных продавцов
        manufacturers: [], // список выбранных производителей
        specifications: [],
      },
      sellers: [], // список всех продавцов
      manufacturers: [], // список всех производителей
      specifications: [],
    };
  },
};

