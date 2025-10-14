# 최종 모델 학습

# cv : 그리드 서치로 최종 모델 & 파라미터 json 저장 : train 학습, vaild 평가
# train : 저장된 json으로 단일모델 저장 (train+valid)
# predict : 저장된 모델pkl로 예측 결과저장 (trn val tst)
# evaluate : 예측결과-> f1, pr, auc , acc 등 (최종 성능 test로 평가)
# main : 데이터전처리 > cv > train > pred > eval