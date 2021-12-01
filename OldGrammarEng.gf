concrete OldGrammarEng of OldGrammar = {

	lincat

		UDS = TODO;
		X = TODO;
		acl = TODO ;
		aclRelcl = TODO ;
		advcl = TODO ;
		advmod = TODO ;
		advmodEmph = TODO ;
		advmodLmod = TODO ;
		amod = TODO ;
		appos = TODO ;
		aux = TODO ;
		auxPass = TODO ;
		case_ = TODO ;
		cc = TODO ;
		ccPreconj = TODO ;
		ccomp = TODO ;
		clf = TODO ;
		compound = TODO ;
		compoundLvc = TODO ;
		compoundPrt = TODO ;
		compoundRedup = TODO ;
		compoundSvc = TODO ;
		conj = TODO ;
		cop = TODO ;
		csubj = TODO ;
		csubjPass = TODO ;
		dep = TODO ;
		det = TODO ;
		detNumgov = TODO ;
		detNummod = TODO ;
		detPoss = TODO ;
		discourse = TODO ;
		dislocated = TODO ;
		expl = TODO ;
		explImpers = TODO ;
		explPass = TODO ;
		explPv = TODO ;
		fixed = TODO ;
		flat = TODO ;
		flatForeign = TODO ;
		flatName = TODO ;
		goeswith = TODO ;
		iobj = TODO ;
		list = TODO ;
		mark = TODO ;
		nmod = TODO ;
		nmodPoss = TODO ;
		nmodTmod = TODO ;
		nsubj = TODO ;
		nsubjPass = TODO ;
		nummod = TODO ;
		nummodGov = TODO ;
		obj = TODO ;
		obl = TODO ;
		oblAgent = TODO ;
		oblArg = TODO ;
		oblLmod = TODO ;
		oblTmod = TODO ;
		orphan = TODO ;
		parataxis = TODO ;
		punct = TODO ;
		reparandum = TODO ;
		root = TODO ;
		vocative = TODO ;
		xcomp = TODO ;

	lin
		-- the coercion funs
		acl_ x = TODO ;
		aclRelcl_ x = TODO ;
		advcl_ x = TODO ;
		advmod_ x = TODO ;
		advmodEmph_ x = TODO ;
		advmodLmod_ x = TODO ;
		amod_ x = TODO ;
		appos_ x = TODO ;
		aux_ x = TODO ;
		auxPass_ x = TODO ;
		case__ x = TODO ;
		cc_ x = TODO ;
		ccPreconj_ x = TODO ;
		ccomp_ x = TODO ;
		clf_ x = TODO ;
		compound_ x = TODO ;
		compoundLvc_ x = TODO ;
		compoundPrt_ x = TODO ;
		compoundRedup_ x = TODO ;
		compoundSvc_ x = TODO ;
		conj_ x = TODO ;
		cop_ x = TODO ;
		csubj_ x = TODO ;
		csubjPass_ x = TODO ;
		dep_ x = TODO ;
		det_ x = TODO ;
		detNumgov_ x = TODO ;
		detNummod_ x = TODO ;
		detPoss_ x = TODO ;
		discourse_ x = TODO ;
		dislocated_ x = TODO ;
		expl_ x = TODO ;
		explImpers_ x = TODO ;
		explPass_ x = TODO ;
		explPv_ x = TODO ;
		fixed_ x = TODO ;
		flat_ x = TODO ;
		flatForeign_ x = TODO ;
		flatName_ x = TODO ;
		goeswith_ x = TODO ;
		iobj_ x = TODO ;
		list_ x = TODO ;
		mark_ x = TODO ;
		nmod_ x = TODO ;
		nmodPoss_ x = TODO ;
		nmodTmod_ x = TODO ;
		nsubj_ x = TODO ;
		nsubjPass_ x = TODO ;
		nummod_ x = TODO ;
		nummodGov_ x = TODO ;
		obj_ x = TODO ;
		obl_ x = TODO ;
		oblAgent_ x = TODO ;
		oblArg_ x = TODO ;
		oblLmod_ x = TODO ;
		oblTmod_ x = TODO ;
		orphan_ x = TODO ;
		parataxis_ x = TODO ;
		punct_ x = TODO ;
		reparandum_ x = TODO ;
		root_ x = TODO ;
		vocative_ x = TODO ;
		xcomp_ x = TODO ;

		-- the actual funs
		-- : root -> advcl -> det -> compound -> amod -> advcl
		root_advcl_det_compound_amod_advcl root advcl det compound amod advcl = TODO ;
		-- : root -> advcl -> nsubjPass -> auxPass
		root_advcl_nsubjPass_auxPass root advcl nsubjPass auxPass = TODO ;
		-- : root -> advcl -> nsubj -> aux -> advcl
		root_advcl_nsubj_aux_advcl root advcl nsubj aux advcl = TODO ;
		-- : root -> advcl -> nsubj -> aux -> advmod -> obj
		root_advcl_nsubj_aux_advmod_obj root advcl nsubj aux advmod obj = TODO ;
		-- : root -> advcl -> nsubj -> aux -> ccomp
		root_advcl_nsubj_aux_ccomp root advcl nsubj aux ccomp = TODO ;
		-- : root -> advcl -> nsubj -> aux -> obj -> advmod -> conj
		root_advcl_nsubj_aux_obj_advmod_conj root advcl nsubj aux obj advmod conj = TODO ;
		-- : root -> advcl -> nsubj -> aux -> obl -> obj
		root_advcl_nsubj_aux_obl_obj root advcl nsubj aux obl obj = TODO ;
		-- : root -> advcl -> nsubj -> conj
		root_advcl_nsubj_conj root advcl nsubj conj = TODO ;
		-- : root -> advcl -> nsubj -> cop
		root_advcl_nsubj_cop root advcl nsubj cop = TODO ;
		-- : root -> advcl -> nsubj -> cop -> case_ -> amod -> nmod
		root_advcl_nsubj_cop_case_amod_nmod root advcl nsubj cop case_ amod nmod = TODO ;
		-- : root -> advcl -> nsubj -> cop -> det -> amod
		root_advcl_nsubj_cop_det_amod root advcl nsubj cop det amod = TODO ;
		-- : root -> advcl -> nsubj -> xcomp
		root_advcl_nsubj_xcomp root advcl nsubj xcomp = TODO ;
		-- : root -> det -> compound -> nmod -> parataxis
		root_det_compound_nmod_parataxis root det compound nmod parataxis = TODO ;
		-- : root -> mark -> nsubj -> nsubj -> xcomp
		root_mark_nsubj_nsubj_xcomp root mark nsubj nsubj xcomp = TODO ;
		-- : root -> nsubjPass -> auxPass -> advmod -> advcl
		root_nsubjPass_auxPass_advmod_advcl root nsubjPass auxPass advmod advcl = TODO ;
		-- : root -> nsubjPass -> auxPass -> advmod -> xcomp
		root_nsubjPass_auxPass_advmod_xcomp root nsubjPass auxPass advmod xcomp = TODO ;
		-- : root -> nsubjPass -> auxPass -> xcomp
		root_nsubjPass_auxPass_xcomp root nsubjPass auxPass xcomp = TODO ;
		-- : root -> nsubjPass -> aux -> auxPass
		root_nsubjPass_aux_auxPass root nsubjPass aux auxPass = TODO ;
		-- : root -> nsubjPass -> aux -> auxPass -> obl -> advmod
		root_nsubjPass_aux_auxPass_obl_advmod root nsubjPass aux auxPass obl advmod = TODO ;
		-- : root -> nsubjPass -> aux -> auxPass -> obl -> conj
		root_nsubjPass_aux_auxPass_obl_conj root nsubjPass aux auxPass obl conj = TODO ;
		-- : root -> nsubjPass -> aux -> auxPass -> obl -> obl -> advcl
		root_nsubjPass_aux_auxPass_obl_obl_advcl root nsubjPass aux auxPass obl obl advcl = TODO ;
		-- : root -> nsubjPass -> aux -> auxPass -> obl -> obl -> advmod
		root_nsubjPass_aux_auxPass_obl_obl_advmod root nsubjPass aux auxPass obl obl advmod = TODO ;
		-- : root -> nsubj -> aux -> advmod -> obj -> advcl
		root_nsubj_aux_advmod_obj_advcl root nsubj aux advmod obj advcl = TODO ;
		-- : root -> nsubj -> aux -> obj -> conj -> parataxis
		root_nsubj_aux_obj_conj_parataxis root nsubj aux obj conj parataxis = TODO ;
		-- : root -> nsubj -> aux -> obj -> obl -> advmod -> advcl
		root_nsubj_aux_obj_obl_advmod_advcl root nsubj aux obj obl advmod advcl = TODO ;
		-- : root -> nsubj -> aux -> obj -> obl -> obl
		root_nsubj_aux_obj_obl_obl root nsubj aux obj obl obl = TODO ;
		-- : root -> nsubj -> cop
		root_nsubj_cop root nsubj cop = TODO ;
		-- : root -> nsubj -> cop -> aclRelcl
		root_nsubj_cop_aclRelcl root nsubj cop aclRelcl = TODO ;
		-- : root -> nsubj -> cop -> advcl -> conj
		root_nsubj_cop_advcl_conj root nsubj cop advcl conj = TODO ;
		-- : root -> nsubj -> cop -> det -> aclRelcl
		root_nsubj_cop_det_aclRelcl root nsubj cop det aclRelcl = TODO ;
		-- : root -> nsubj -> cop -> det -> amod -> advcl
		root_nsubj_cop_det_amod_advcl root nsubj cop det amod advcl = TODO ;
		-- : root -> nsubj -> cop -> det -> amod -> compound
		root_nsubj_cop_det_amod_compound root nsubj cop det amod compound = TODO ;
		-- : root -> nsubj -> cop -> det -> amod -> conj -> conj -> conj -> conj -> conj -> conj
		root_nsubj_cop_det_amod_conj_conj_conj_conj_conj_conj root nsubj cop det amod conj conj conj conj conj conj = TODO ;
		-- : root -> nsubj -> cop -> det -> nmod
		root_nsubj_cop_det_nmod root nsubj cop det nmod = TODO ;
		-- : root -> nsubj -> cop -> obl -> parataxis
		root_nsubj_cop_obl_parataxis root nsubj cop obl parataxis = TODO ;
		-- : root -> nsubj -> obj
		root_nsubj_obj root nsubj obj = TODO ;
		-- : root -> nsubj -> obj -> advcl
		root_nsubj_obj_advcl root nsubj obj advcl = TODO ;
}
