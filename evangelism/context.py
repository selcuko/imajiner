from datetime import date

year = date.today().year

def SiteWideContextSupplier(request):
    return {
        'doc': {
            'title': 'Bağlam Uygulandı',
        },
        'copyright': f'Copyright &copy; {year} Tüm hakları saklıdır.',
        'credits': f"Site stili büyük oranda <a class=\"philosophy\" href=\"https://colorlib.com\">Colorlib</a>'den alınmıştır. <a class=\"philosophy\" href=\"#0\">Detaylı bilgi</a>"
    }