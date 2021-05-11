#!/bin/bash


if [[ -z $1 ]]; then
	echo "[!] ERROR: Missing dictionary file"
	exit 1
fi

if [[ -z $2 ]]; then
	echo "[!] Missing reference file"
	exit 2
fi

DICT=$1
REFL=$2

CHKSUM="md5"
if [[ $3 ]]; then
	CHKSUM=$3
fi

SYSTYPE=$(uname -s)
if [[ ${SYSTYPE} == "Darwin" ]]; then

	if [[ ${CHKSUM} == "md5" ]];  then
		CHKSUM="md5"
	elif [[ ${CHKSUM} == "sha1" ]];  then
		CHKSUM="shasum"
	elif [[ ${CHKSUM} == "sha256" ]];  then
			CHKSUM="sha2 -256"
	else
		echo "[!≈] Unsupported checksum type"
		exit 16
	fi

elif [[ ${SYSTYPE} == "Linux" ]]; then

	if [[ ${CHKSUM} == "md5" ]];  then
		CHKSUM="md5sum"
	elif [[ ${CHKSUM} == "sha1" ]];  then
		CHKSUM="sha1sum"
	elif [[ ${CHKSUM} == "sha256" ]];  then
		CHKSUM="sha256sum"
	else
		echo "[!≈] Unsupported checksum type"
		exit 16
	fi

else
	echo "[!] Unsupported system type ${SYSTYPE}"
	exit 10
fi


echo "[-] Using dictionary file ${DICT}"
echo "[-] Using reference file ${REFL}"
echo "[-] Using checksum ${CHKSUM}"

for R in $( cat ${REFL} ); do
	UNAME=$( echo $R|cut -d: -f 1 )
	HSHPWD=$( echo $R|cut -d: -f 2 )

	if [[ ${#R} ]]; then

		for D in $( cat ${DICT} ); do
			if [[ ${#D} ]]; then
				DEC=$D
				COD=$( echo $D|$CHKSUM|cut -d' ' -f 1)
				echo -ne "[ ] Checking $D - ${HSHPWD} - ${COD}                             \r"

				if [[ "${HSHPWD}" == "${COD}" ]]; then
					echo "[+] $UNAME: $DEC"
				fi
			fi
		done

	fi
done
