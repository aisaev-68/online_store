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
       const url = '/api/specification/' + this.category + '/';
        this.getData(url)
          .then((data) => {
            this.specifications = data;
            //alert(JSON.stringify(this.specifications));
          })
          .catch(() => {
            this.specifications = [];
            console.warn('Ошибка получения спецификаций');
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
      updateSpecifications() {

        this.filter.specifications = this.specifications.filter((specification) =>
        this.selectedSpecifications.includes(specification.id)

        );
      },
      updateManufacturers() {
        this.filter.manufacturers = this.manufacturers.filter((manufacturer) =>
          this.selectedManufacturers.includes(manufacturer.id)
        );
        //this.getCatalogs();
      },
      updateSellers() {
        this.filter.sellers = this.sellers.filter((seller) =>
          this.selectedSellers.includes(seller.id)
        );
        //this.getCatalogs();
      },
    getTags() {
      this.getData('/api/tags', { category: this.category })
        .then((data) => (this.topTags = data.map((tag) => ({ ...tag, selected: false }))))
        .catch(() => {
          this.topTags = [];
          console.warn('Ошибка получения тегов');
        });
    },
    getCatalogs(page, filterSearch) {
      if (typeof page === 'undefined') {
        page = 1;
      }
      const PAGE_LIMIT = 6;
      const tags = this.topTags
        .filter((tag) => tag.selected)
        .map((tag) => tag.id);

      const params = new URLSearchParams(window.location.search);

      // Установка параметров запроса в адресной строке
      params.set('page', page.toString());
      if (typeof filterSearch !== 'undefined') {
        params.set('filterSearch', filterSearch);
      }
      if (this.selectedSort) {
        params.set('sort', this.selectedSort.id);
        params.set('sortType', this.selectedSort.selected);
      }

      if (this.filter.name) {
        params.set('filter.name', this.filter.name);
      }
      if (this.filter.minPrice) {
        params.set('filter.minPrice', this.filter.minPrice.toString());
      }
      //alert(this.filter.maxPrice);
      if (this.filter.maxPrice) {
        params.set('filter.maxPrice', this.filter.maxPrice.toString());
      }
//      if (this.filter.freeDelivery) {
//        params.set('filter.freeDelivery', this.filter.freeDelivery.toString());
//      }
//      if (this.filter.available) {
//        params.set('filter.available', this.filter.available.toString());
//      }
      this.getData('/api/catalog/', {
        page,
        filterSearch: this.filterSearch ? this.filterSearch : null,
        category: this.category ? this.category : null,
        sort: this.selectedSort ? this.selectedSort.id : null,
        sortType: this.selectedSort ? this.selectedSort.selected : null,
        filter: {
          name: this.filter.name ? this.filter.name : null,
          minPrice: this.filter.minPrice ? this.filter.minPrice : null,
          maxPrice: this.filter.maxPrice ? this.filter.maxPrice : null,
          freeDelivery: this.filter.freeDelivery ? this.filter.freeDelivery : null,
          available: this.filter.available ? this.filter.available : null,
          sellers: this.filter.sellers ? this.filter.sellers : null,
          manufacturers: this.filter.manufacturers ? this.filter.manufacturers : null,
          specifications: this.filter.specifications ? this.filter.specifications : null,
        },
        tags,
        limit: PAGE_LIMIT,
      })
        .then((data) => {
          this.catalogCards = data.items;
          this.currentPage = data.currentPage;
          this.lastPage = data.lastPage;

          // Обновление адресной строки
          window.history.replaceState(null, null, '?' + params.toString());
          this.resetFilters();
          //this.updateURL();
        })
        .catch(() => {
          console.warn('Ошибка при получении каталога');
        });
    },
    resetFilters() {
        this.filter = {
          name: '',
          minPrice: 1,
          maxPrice: 30000,
          freeDelivery: false,
          available: true,
          sellers: [],
          manufacturers: [],
          specifications: [],
        };
  },
    updateURL() {
      const params = new URLSearchParams();
      params.set('filter.freeDelivery', this.filter.freeDelivery.toString());
      params.set('filter.available', this.filter.available.toString());

      if (this.filter.specifications && this.filter.specifications.length > 0) {
        // Удаление предыдущих значений
        this.filter.specifications.forEach((specification) => {
          params.delete(`filter.specifications.${specification.key}`);
        });

        // Добавление новых значений
        this.filter.specifications.forEach((specification) => {
          params.append(`filter.specifications.${specification.key}`, specification.value);
        });
          } else {
            // Если фильтр specifications пуст, удалить ключ filter.specifications
            params.delete('filter.specifications');
          }

          if (this.filter.sellers && this.filter.sellers.length > 0) {
            let prefix = 'filter.sellers';
            let i = 0;
            while (params.has(prefix)) {
              params.delete(`${prefix}[${i}]`);
              i++;
            }
            this.filter.sellers.forEach((seller, index) => {
              params.set(`filter.sellers[${index}]`, seller);
            });
          } else {
            params.delete('filter.sellers');
          }

          if (this.filter.manufacturers && this.filter.manufacturers.length > 0) {
            let prefix = 'filter.manufacturers';
            let i = 0;
            while (params.has(prefix)) {
              params.delete(`${prefix}[${i}]`);
              i++;
            }
            this.filter.manufacturers.forEach((manufacturer, index) => {
              params.set(`filter.manufacturers[${index}]`, manufacturer);
            });
          } else {
            params.delete('filter.manufacturers');
          }
          const newURL = this.currentURL + '&' + params.toString();
          window.history.pushState(null, null, newURL);
         },
      updateFilterPrice(data) {
      // data - объект с полями from и to, содержащими текущие значения ползунка
      this.filter.minPrice = data.from;
      this.filter.maxPrice = data.to;
    },
    initRangeSlider() {
      var $range = $('.range'),
        $line = $range.find('.range-line');

      $line.ionRangeSlider({
        onStart: function (data) {
          $('.rangePrice').text('₽' + data.from + ' - ₽' + data.to);
        },
        onChange: (data) => {
          $('.rangePrice').text('₽' + data.from + ' - ₽' + data.to);
          this.updateFilterPrice(data);
        },
      });
    },

   },
  mounted() {
    this.initRangeSlider();
    const urlParams = new URL(window.location.href).searchParams;
    this.filterSearch = urlParams.get('filterSearch');
    this.category = urlParams.get('category') ? Number(urlParams.get('category')) : null;
    this.selectedSort = this.sortRules.find((sort) => sort.id === 'price');
    this.selectedSort.selected = 'inc';
    this.getCatalogs();
    this.getTags();
    this.getSellers();
    this.getManufacturers();
    this.updateSellers();
    this.updateManufacturers();
    this.getSpecifications();
    this.updateSpecifications();

  },

  data() {
    return {
      pages: 1,
      filterSearch: '',
      category: null,
      catalogCards: [],
      currentPage: null,
      lastPage: 1,
      selectedSort: null,
      filter: {
        name: '',
        minPrice: 1,
        maxPrice: 30000,
        freeDelivery: false,
        available: true,
        sellers: [], // список выбранных продавцов
        manufacturers: [], // список выбранных производителей
        specifications: [],
//        minValue: 0,
//        maxValue: 0,
      },
      currentURL: window.location.href,
      sellers: [], // список всех продавцов
      manufacturers: [], // список всех производителей
      specifications: [],
    };
  },
};

