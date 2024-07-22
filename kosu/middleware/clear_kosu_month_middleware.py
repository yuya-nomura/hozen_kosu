from django.utils.deprecation import MiddlewareMixin





class ClearKosuMonthMiddleware(MiddlewareMixin):
  def process_request(self, request):
    # '/list/' と '/detail/' パスを含むURLの場合、セッションをクリアしない
    if not (request.path.startswith('/list/') or request.path.startswith('/detail/')):
      if 'kosu_month' in request.session:
        del request.session['kosu_month']