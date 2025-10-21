from django.shortcuts import render, get_object_or_404
from .models import *
from PIL import Image
from django.db.models import Sum


# Create your views here.
# ========== Peta Page =========
def data_teknis_view(request):
    data = PetaDIModel.objects.all()

    context = {
        "pageName": "dataTeknis",
        "data": data,
        "titlePage": "Peta",
        "heroTitle": "Peta D.I. Oransbari",
    }
    return render(request, "datateknis/peta_page.html", context)


# ========== Peta Page =========
def detail_peta_view(request, peta_id):

    data = PetaDIModel.objects.get(pk=peta_id)

    context = {
        "pageName": "dataTeknis",
        "data": data,
        "titlePage": "Peta",
        "heroTitle": "Peta D.I. Oransbari",
    }
    return render(request, "datateknis/detail_peta_page.html", context)


# ========== Sumber Air Page Ketersediaan Air =========
def sumber_air_view(request):
    data_bendung = BendungModel.objects.all()
    data_embung = EmbungModel.objects.order_by("-id")[:5]
    data_ketersediaan_air = KetersediaanAirModel.objects.all()

    context = {
        "pageName": "dataTeknis",
        "titlePage": "Ketersediaan Air",
        "bendung": data_bendung,
        "embung": data_embung,
        "ketersediaanAir": data_ketersediaan_air,
        "heroTitle": "Data Teknis",
        "heroSubtitle": "#Sumber Air Irigasi",
    }

    return render(request, "datateknis/sumber_air_page.html", context)


# ========== Sumber Air Page Bendung =========
def bendung_view(request):

    data = BendungModel.objects.all()

    context = {
        "pageName": "dataTeknis",
        "data": data,
        "titlePage": "Bendung",
        "heroTitle": "Sumber Air Irigasi",
        "heroSubtitle": "#Bendung",
    }

    return render(request, "datateknis/bendung_page.html", context)


# ========== Sumber Air Page Bendung =========
def detail_bendung_view(request, bendung_id):

    data = BendungModel.objects.get(pk=bendung_id)

    context = {
        "pageName": "dataTeknis",
        "titlePage": "Bendung",
        "data": data,
        "heroTitle": "Sumber Air Irigasi",
        "heroSubtitle": "#Bendung",
    }

    return render(request, "datateknis/detail_bendung_page.html", context)


# ========== Sumber Air Page Embung =========
def embung_view(request):
    data = EmbungModel.objects.all()

    context = {
        "pageName": "dataTeknis",
        "titlePage": "Embung",
        "data": data,
        "heroTitle": "Sumber Air Irigasi",
        "heroSubtitle": "#Embung",
    }

    return render(request, "datateknis/embung_page.html", context)


# NOTE: ============> SKEMA VIEW
def skema_view(reques):

    data_skema = SkemaModel.objects.order_by("-id").all()
    context = {
        "pageName": "dataTeknis",
        "titlePage": "Skema",
        "heroTitle": "Data Teknis",
        "heroSubtitle": "#Skema",
        "data": data_skema,
    }

    return render(reques, "datateknis/skema_page.html", context)


# NOTE: ============> JARINGAN IRIGASI UTAMA
# NOTE: ==>Jaringan Premier<==
def jaringan_primer_view(request):
    jaringan = get_object_or_404(JenisJaringanModel, kode="B.WR")
    ruas_list = jaringan.primer.select_related("bangunan_1", "bangunan_2").all()
    # print(f"Jaringan => {ruas_list}")
    data_premier = JaringanPrimerModel.objects.all()
    total_panjang_saluran = JaringanPrimerModel.total_panjang()
    context = {
        "pageName": "dataTeknis",
        "titlePage": "Jaringan Irigasi Utama",
        "heroTitle": "Data Teknis",
        "heroSubtitle": "#Jaringan Irigasi Utama | Primer",
        "data": data_premier,
        "totalPanjang": round(total_panjang_saluran, 2),
        "jaringan": jaringan,
        "ruasList": ruas_list,
    }

    return render(request, "datateknis/jaringan_primer_page.html", context)


# NOTE: ==>Jaringan Sekunder<==
def jaringan_sekunder_view(request):

    # Jaringan Sekunder Warbiadi B.WR.5
    jaringan_bwr_5 = get_object_or_404(JenisJaringanModel, kode="B.WR.5")
    ruas_list_bwr_5 = jaringan_bwr_5.sekunder.select_related(
        "bangunan_1", "bangunan_2"
    ).all()
    total_panjang_bwr_5 = JaringanSekunderModel.total_panjang_b_wr_5()

    # Jaringan Sekunder Warbiadi B.WR.5.1
    jaringan_bwr_5_1 = get_object_or_404(JenisJaringanModel, kode="B.WR.5.1")
    ruas_list_bwr_5_1 = jaringan_bwr_5_1.sekunder.select_related(
        "bangunan_1", "bangunan_2"
    ).all()
    total_panjang_bwr_5_1 = JaringanSekunderModel.total_panjang_b_wr_5_1()

    # Jaringan Sekunder Sindang Jaya S.J
    jaringan_bsj = get_object_or_404(JenisJaringanModel, kode="B.SJ")
    ruas_list_bsj = jaringan_bsj.sekunder.select_related(
        "bangunan_1", "bangunan_2"
    ).all()
    total_panjang_bsj = JaringanSekunderModel.total_panjang_b_sj()

    # Jaringan Sekunder Margomulyo B.M
    jaringan_bm = get_object_or_404(JenisJaringanModel, kode="B.M")
    ruas_list_bm = jaringan_bm.sekunder.select_related("bangunan_1", "bangunan_2").all()
    total_panjang_bm = JaringanSekunderModel.total_panjang_b_m()

    # Jaringan Sekunder Oransbari B.OR
    jaringan_bor = get_object_or_404(JenisJaringanModel, kode="B.OR")
    ruas_list_bor = jaringan_bor.sekunder.select_related(
        "bangunan_1", "bangunan_2"
    ).all()
    total_panjang_bor = JaringanSekunderModel.total_panjang_b_or()

    context = {
        "pageName": "dataTeknis",
        "titlePage": "Jaringan Irigasi Utama",
        "heroTitle": "Data Teknis",
        "heroSubtitle": "#Jaringan Irigasi Utama | Sekunder",
        "ruasBWR5": ruas_list_bwr_5,
        "totalPanjangBWR5": total_panjang_bwr_5,
        "ruasBWR51": ruas_list_bwr_5_1,
        "totalPanjangBWR51": total_panjang_bwr_5_1,
        "ruasBSJ": ruas_list_bsj,
        "totalPanjangBSJ": total_panjang_bsj,
        "ruasBM": ruas_list_bm,
        "totalPanjangBM": total_panjang_bm,
        "ruasBOR": ruas_list_bor,
        "totalPanjangBOR": total_panjang_bor,
    }

    return render(request, "datateknis/jaringan_sekunder_page.html", context)


# NOTE: ==>Jaringan Sekunder<==
def jaringan_tersier_view(request):
    data = JaringanTersierModel.objects.all()
    total_luasan = round(JaringanTersierModel.total_luasan(), 2)
    context = {
        "pageName": "dataTeknis",
        "titlePage": "Jaringan Irigasi Utama",
        "heroTitle": "Data Teknis",
        "heroSubtitle": "#Jaringan Irigasi Utama | Tersier",
        "dataTersier": data,
        "totalLuasan": total_luasan,
    }

    return render(request, "datateknis/jaringan_tersier_page.html", context)


# NOTE: ============> PETUGAS OP
def petugas_op_view(request):
    data_petugas = PetugasOPModel.objects.all()
    context = {
        "pageName": "dataTeknis",
        "titlePage": "Petugas OP",
        "heroTitle": "Data Teknis",
        "heroSubtitle": "#Petugas Operasi & Pemeliharaan",
        "dataPetugas": data_petugas,
    }
    return render(request, "datateknis/petugas_op_page.html", context)


def detail_petugas_op_view(request, petugas_id):

    data_petugas = PetugasOPModel.objects.filter(pk=petugas_id).first()
    bangunan = data_petugas.bangunan.all()
    print(f"Data Bangunan => {bangunan}")
    context = {
        "pageName": "dataTeknis",
        "titlePage": "Petugas OP",
        "heroTitle": "Data Teknis",
        "heroSubtitle": "#Petugas Operasi & Pemeliharaan",
        "dataPetugas": data_petugas,
        "bangunan": bangunan,
    }

    return render(request, "datateknis/detail_petugas_op_page.html", context)
